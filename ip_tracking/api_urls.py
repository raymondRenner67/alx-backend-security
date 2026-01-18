"""
API URL Configuration for REST endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ip_tracking import api_views

router = DefaultRouter()
router.register(r'request-logs', api_views.RequestLogViewSet, basename='requestlog')
router.register(r'blocked-ips', api_views.BlockedIPViewSet, basename='blockedip')
router.register(r'suspicious-ips', api_views.SuspiciousIPViewSet, basename='suspiciousip')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', api_views.StatisticsAPIView.as_view(), name='stats'),
]
