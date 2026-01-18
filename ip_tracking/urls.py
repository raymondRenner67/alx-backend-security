from django.urls import path
from . import views

app_name = 'ip_tracking'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('api/sensitive/', views.sensitive_api_view, name='sensitive_api'),
]
