from django.db import models


class RequestLog(models.Model):
    """
    Model to store request logs with IP address, timestamp, path, and geolocation data.
    """
    ip_address = models.GenericIPAddressField(
        help_text="IP address of the client making the request"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the request was made"
    )
    path = models.CharField(
        max_length=500,
        help_text="URL path of the request"
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Country of the IP address"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City of the IP address"
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Request Log'
        verbose_name_plural = 'Request Logs'

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"


class BlockedIP(models.Model):
    """
    Model to store blocked IP addresses.
    """
    ip_address = models.GenericIPAddressField(
        unique=True,
        help_text="IP address to block"
    )
    reason = models.TextField(
        blank=True,
        null=True,
        help_text="Reason for blocking this IP address"
    )
    blocked_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the IP was blocked"
    )

    class Meta:
        ordering = ['-blocked_at']
        verbose_name = 'Blocked IP'
        verbose_name_plural = 'Blocked IPs'

    def __str__(self):
        return f"{self.ip_address}"


class SuspiciousIP(models.Model):
    """
    Model to store suspicious IP addresses flagged by anomaly detection.
    """
    ip_address = models.GenericIPAddressField(
        help_text="Suspicious IP address"
    )
    reason = models.TextField(
        help_text="Reason why this IP was flagged as suspicious"
    )
    flagged_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the IP was flagged"
    )
    resolved = models.BooleanField(
        default=False,
        help_text="Whether this suspicious activity has been reviewed/resolved"
    )

    class Meta:
        ordering = ['-flagged_at']
        verbose_name = 'Suspicious IP'
        verbose_name_plural = 'Suspicious IPs'

    def __str__(self):
        return f"{self.ip_address} - {self.reason[:50]}"
