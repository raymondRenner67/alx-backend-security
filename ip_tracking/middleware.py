from .models import RequestLog


class IPTrackingMiddleware:
    """
    Middleware to log IP address, timestamp, and path of every incoming request.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client IP address
        ip_address = self.get_client_ip(request)
        
        # Get the request path
        path = request.path
        
        # Log the request
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path
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
