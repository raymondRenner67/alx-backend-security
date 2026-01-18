from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited


@ratelimit(key='ip', rate='5/m', method='POST')
@ratelimit(key='user_or_ip', rate='10/m', method='POST')
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Login view with rate limiting:
    - 5 requests per minute for anonymous users (by IP)
    - 10 requests per minute for authenticated users
    """
    if request.method == 'GET':
        return render(request, 'ip_tracking/login.html')
    
    # POST request - handle login
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if not username or not password:
        return JsonResponse({
            'success': False,
            'error': 'Username and password are required'
        }, status=400)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return JsonResponse({
            'success': True,
            'message': 'Login successful'
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Invalid credentials'
        }, status=401)


@ratelimit(key='ip', rate='5/m', method='POST')
@ratelimit(key='user_or_ip', rate='10/m', method='POST')
@require_http_methods(["POST"])
def sensitive_api_view(request):
    """
    Example of a sensitive API endpoint with rate limiting.
    - 5 requests per minute for anonymous users
    - 10 requests per minute for authenticated users
    """
    try:
        # Your sensitive operation here
        return JsonResponse({
            'success': True,
            'message': 'Operation completed successfully'
        })
    except Ratelimited:
        return JsonResponse({
            'success': False,
            'error': 'Rate limit exceeded. Please try again later.'
        }, status=429)


def rate_limit_handler(request, exception):
    """
    Custom handler for rate limit exceptions.
    """
    return JsonResponse({
        'success': False,
        'error': 'Rate limit exceeded. Please try again later.',
        'retry_after': getattr(exception, 'retry_after', 60)
    }, status=429)
