"""
API Views and Serializers for IP Tracking Application.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .models import RequestLog, BlockedIP, SuspiciousIP
from .serializers import (
    RequestLogSerializer,
    BlockedIPSerializer,
    SuspiciousIPSerializer,
    StatisticsSerializer,
)


@extend_schema(tags=['Request Logs'])
class RequestLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing request logs.
    Provides list and detail views of all logged requests with geolocation data.
    """
    queryset = RequestLog.objects.all().order_by('-timestamp')
    serializer_class = RequestLogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['ip_address', 'country', 'city']
    search_fields = ['ip_address', 'path', 'country', 'city']
    
    @extend_schema(
        description="Get request logs for a specific IP address",
        parameters=[
            OpenApiParameter(
                name='ip',
                type=str,
                location=OpenApiParameter.PATH,
                description='IP address to filter by'
            ),
        ],
    )
    @action(detail=False, methods=['get'], url_path='by-ip/(?P<ip>[^/.]+)')
    def by_ip(self, request, ip=None):
        """Get all logs for a specific IP address"""
        logs = self.queryset.filter(ip_address=ip)
        page = self.paginate_queryset(logs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Blocked IPs'])
class BlockedIPViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing blocked IP addresses.
    Allows creating, viewing, updating, and deleting blocked IPs.
    """
    queryset = BlockedIP.objects.all().order_by('-blocked_at')
    serializer_class = BlockedIPSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['ip_address']
    search_fields = ['ip_address', 'reason']
    
    @extend_schema(
        description="Check if an IP address is blocked",
        parameters=[
            OpenApiParameter(
                name='ip',
                type=str,
                location=OpenApiParameter.PATH,
                description='IP address to check'
            ),
        ],
    )
    @action(detail=False, methods=['get'], url_path='check/(?P<ip>[^/.]+)')
    def check_blocked(self, request, ip=None):
        """Check if a specific IP is blocked"""
        is_blocked = self.queryset.filter(ip_address=ip).exists()
        if is_blocked:
            blocked_ip = self.queryset.get(ip_address=ip)
            serializer = self.get_serializer(blocked_ip)
            return Response({
                'blocked': True,
                'details': serializer.data
            })
        return Response({'blocked': False})


@extend_schema(tags=['Suspicious IPs'])
class SuspiciousIPViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing suspicious IP addresses flagged by anomaly detection.
    """
    queryset = SuspiciousIP.objects.all().order_by('-flagged_at')
    serializer_class = SuspiciousIPSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['ip_address', 'resolved']
    search_fields = ['ip_address', 'reason']
    
    @extend_schema(description="Mark a suspicious IP as resolved")
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark a suspicious IP flag as resolved"""
        suspicious_ip = self.get_object()
        suspicious_ip.resolved = True
        suspicious_ip.save()
        serializer = self.get_serializer(suspicious_ip)
        return Response(serializer.data)
    
    @extend_schema(description="Get all unresolved suspicious IPs")
    @action(detail=False, methods=['get'])
    def unresolved(self, request):
        """Get all unresolved suspicious IP flags"""
        unresolved = self.queryset.filter(resolved=False)
        page = self.paginate_queryset(unresolved)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(unresolved, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Statistics'])
class StatisticsAPIView(APIView):
    """
    API view for getting statistics about IP tracking.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @extend_schema(
        description="Get comprehensive statistics about IP tracking",
        responses={200: StatisticsSerializer},
    )
    def get(self, request):
        """Get statistics about requests, blocked IPs, and suspicious activity"""
        now = timezone.now()
        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)
        
        stats = {
            'total_requests': RequestLog.objects.count(),
            'requests_last_hour': RequestLog.objects.filter(timestamp__gte=last_hour).count(),
            'requests_last_day': RequestLog.objects.filter(timestamp__gte=last_day).count(),
            'unique_ips_total': RequestLog.objects.values('ip_address').distinct().count(),
            'unique_ips_last_day': RequestLog.objects.filter(
                timestamp__gte=last_day
            ).values('ip_address').distinct().count(),
            'blocked_ips_count': BlockedIP.objects.count(),
            'suspicious_ips_total': SuspiciousIP.objects.count(),
            'suspicious_ips_unresolved': SuspiciousIP.objects.filter(resolved=False).count(),
            'top_countries': list(
                RequestLog.objects.exclude(country__isnull=True)
                .values('country')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
            ),
            'top_paths': list(
                RequestLog.objects.values('path')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
            ),
            'timestamp': now.isoformat(),
        }
        
        serializer = StatisticsSerializer(data=stats)
        serializer.is_valid()
        return Response(serializer.data)
