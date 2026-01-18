"""
Serializers for IP Tracking API.
"""

from rest_framework import serializers
from .models import RequestLog, BlockedIP, SuspiciousIP


class RequestLogSerializer(serializers.ModelSerializer):
    """Serializer for RequestLog model"""
    
    class Meta:
        model = RequestLog
        fields = ['id', 'ip_address', 'timestamp', 'path', 'country', 'city']
        read_only_fields = ['id', 'timestamp']


class BlockedIPSerializer(serializers.ModelSerializer):
    """Serializer for BlockedIP model"""
    
    class Meta:
        model = BlockedIP
        fields = ['id', 'ip_address', 'reason', 'blocked_at']
        read_only_fields = ['id', 'blocked_at']
    
    def validate_ip_address(self, value):
        """Validate IP address format"""
        import ipaddress
        try:
            ipaddress.ip_address(value)
        except ValueError:
            raise serializers.ValidationError("Invalid IP address format")
        return value


class SuspiciousIPSerializer(serializers.ModelSerializer):
    """Serializer for SuspiciousIP model"""
    
    class Meta:
        model = SuspiciousIP
        fields = ['id', 'ip_address', 'reason', 'flagged_at', 'resolved']
        read_only_fields = ['id', 'flagged_at']


class StatisticsSerializer(serializers.Serializer):
    """Serializer for statistics data"""
    total_requests = serializers.IntegerField()
    requests_last_hour = serializers.IntegerField()
    requests_last_day = serializers.IntegerField()
    unique_ips_total = serializers.IntegerField()
    unique_ips_last_day = serializers.IntegerField()
    blocked_ips_count = serializers.IntegerField()
    suspicious_ips_total = serializers.IntegerField()
    suspicious_ips_unresolved = serializers.IntegerField()
    top_countries = serializers.ListField(child=serializers.DictField())
    top_paths = serializers.ListField(child=serializers.DictField())
    timestamp = serializers.CharField()
