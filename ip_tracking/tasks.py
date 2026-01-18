from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP
import logging

logger = logging.getLogger(__name__)


@shared_task
def detect_anomalies():
    """
    Celery task to detect and flag suspicious IP addresses.
    Runs hourly to identify IPs that:
    1. Exceed 100 requests per hour
    2. Access sensitive paths (e.g., /admin, /login)
    """
    logger.info("Starting anomaly detection task")
    
    # Calculate time range for the last hour
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)
    
    # Define sensitive paths
    sensitive_paths = ['/admin', '/login', '/api/admin', '/api/login', '/admin/', '/login/']
    
    # Flag 1: IPs with more than 100 requests in the last hour
    high_volume_ips = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(request_count=Count('id'))
        .filter(request_count__gt=100)
    )
    
    for ip_data in high_volume_ips:
        ip_address = ip_data['ip_address']
        request_count = ip_data['request_count']
        
        # Check if this IP is already flagged for this reason recently (last 24 hours)
        recent_flag = SuspiciousIP.objects.filter(
            ip_address=ip_address,
            reason__contains='high volume',
            flagged_at__gte=now - timedelta(hours=24),
            resolved=False
        ).exists()
        
        if not recent_flag:
            SuspiciousIP.objects.create(
                ip_address=ip_address,
                reason=f"High volume of requests: {request_count} requests in the last hour"
            )
            logger.warning(f"Flagged IP {ip_address} for high volume: {request_count} requests/hour")
    
    # Flag 2: IPs accessing sensitive paths
    sensitive_access_ips = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago, path__in=sensitive_paths)
        .values('ip_address')
        .annotate(access_count=Count('id'))
        .filter(access_count__gte=5)  # More than 5 attempts to access sensitive paths
    )
    
    for ip_data in sensitive_access_ips:
        ip_address = ip_data['ip_address']
        access_count = ip_data['access_count']
        
        # Get the specific paths accessed
        accessed_paths = (
            RequestLog.objects
            .filter(
                ip_address=ip_address,
                timestamp__gte=one_hour_ago,
                path__in=sensitive_paths
            )
            .values_list('path', flat=True)
            .distinct()
        )
        paths_str = ', '.join(accessed_paths)
        
        # Check if this IP is already flagged for this reason recently
        recent_flag = SuspiciousIP.objects.filter(
            ip_address=ip_address,
            reason__contains='sensitive paths',
            flagged_at__gte=now - timedelta(hours=24),
            resolved=False
        ).exists()
        
        if not recent_flag:
            SuspiciousIP.objects.create(
                ip_address=ip_address,
                reason=f"Multiple attempts to access sensitive paths: {access_count} attempts to [{paths_str}]"
            )
            logger.warning(f"Flagged IP {ip_address} for accessing sensitive paths: {access_count} attempts")
    
    logger.info("Anomaly detection task completed")
    
    return {
        'high_volume_ips_flagged': len(high_volume_ips),
        'sensitive_access_ips_flagged': len(sensitive_access_ips),
        'timestamp': now.isoformat()
    }


@shared_task
def cleanup_old_logs(days=30):
    """
    Optional task to clean up old request logs.
    Removes logs older than specified days (default: 30).
    """
    cutoff_date = timezone.now() - timedelta(days=days)
    deleted_count = RequestLog.objects.filter(timestamp__lt=cutoff_date).delete()[0]
    
    logger.info(f"Cleaned up {deleted_count} old request logs")
    
    return {
        'deleted_count': deleted_count,
        'cutoff_date': cutoff_date.isoformat()
    }
