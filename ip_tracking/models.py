from django.db import models


class RequestLog(models.Model):
    """
    Model to store request logs with IP address, timestamp, and path.
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

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Request Log'
        verbose_name_plural = 'Request Logs'

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"
