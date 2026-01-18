from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import RequestLog, BlockedIP
import requests
import logging

logger = logging.getLogger(__name__)


class IPTrackingMiddleware:
    """
    Middleware to log IP address, timestamp, path, and geolocation data of every incoming request.
    Also blocks requests from blacklisted IPs.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client IP address
        ip_address = self.get_client_ip(request)
        
        # Check if the IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP address has been blocked.")
        
        # Get the request path
        path = request.path
        
        # Get geolocation data (cached for 24 hours)
        geo_data = self.get_geolocation(ip_address)
        
        # Log the request
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            country=geo_data.get('country'),
            city=geo_data.get('city')
        )
        
        # Process the request
        response = self.get_response(request)
        
        return response

    def get_client_ip(self, request):
        """
        Extract the client's IP address from the request.
        Handles cases where the request comes through a proxy.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Get the first IP in the list (client IP)
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Fall back to REMOTE_ADDR
            ip = request.META.get('REMOTE_ADDR')
        
        return ip

    def get_geolocation(self, ip_address):
        """
        Get geolocation data for an IP address.
        Results are cached for 24 hours to reduce API calls.
        """
        # Check cache first (24 hours = 86400 seconds)
        cache_key = f'geo_{ip_address}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        # Default values
        geo_data = {'country': None, 'city': None}
        
        # Skip geolocation for local/private IPs
        if ip_address in ['127.0.0.1', 'localhost', '::1'] or ip_address.startswith('192.168.'):
            cache.set(cache_key, geo_data, 86400)
            return geo_data
        
        try:
            # Using ip-api.com free service (no API key required)
            # For production, consider using django-ipgeolocation or paid service
            response = requests.get(
                f'http://ip-api.com/json/{ip_address}',
                timeout=2
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    geo_data = {
                        'country': data.get('country'),
                        'city': data.get('city')
                    }
        except Exception as e:
            logger.warning(f"Failed to get geolocation for {ip_address}: {str(e)}")
        
        # Cache the result for 24 hours
        cache.set(cache_key, geo_data, 86400)
        
        return geo_data
