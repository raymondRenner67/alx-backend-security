from django.contrib import admin
from .models import RequestLog, BlockedIP, SuspiciousIP


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'country', 'city', 'timestamp')
    list_filter = ('timestamp', 'ip_address', 'country', 'city')
    search_fields = ('ip_address', 'path', 'country', 'city')
    readonly_fields = ('ip_address', 'timestamp', 'path', 'country', 'city')
    
    def has_add_permission(self, request):
        # Prevent manual addition through admin
        return False
    
    def has_change_permission(self, request, obj=None):
        # Prevent manual editing through admin
        return False


@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reason', 'blocked_at')
    list_filter = ('blocked_at',)
    search_fields = ('ip_address', 'reason')
    readonly_fields = ('blocked_at',)


@admin.register(SuspiciousIP)
class SuspiciousIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reason_short', 'flagged_at', 'resolved')
    list_filter = ('flagged_at', 'resolved')
    search_fields = ('ip_address', 'reason')
    readonly_fields = ('ip_address', 'reason', 'flagged_at')
    list_editable = ('resolved',)
    
    def reason_short(self, obj):
        """Display shortened reason in list view"""
        return obj.reason[:75] + '...' if len(obj.reason) > 75 else obj.reason
    reason_short.short_description = 'Reason'
