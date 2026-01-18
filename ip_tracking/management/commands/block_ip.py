from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Block an IP address by adding it to the BlockedIP list'

    def add_arguments(self, parser):
        parser.add_argument(
            'ip_address',
            type=str,
            help='IP address to block (IPv4 or IPv6)'
        )
        parser.add_argument(
            '--reason',
            type=str,
            default='',
            help='Reason for blocking this IP address'
        )

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        reason = options['reason']

        # Validate the IP address
        try:
            validate_ipv46_address(ip_address)
        except ValidationError:
            raise CommandError(f'"{ip_address}" is not a valid IP address')

        # Check if the IP is already blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(
                self.style.WARNING(f'IP address {ip_address} is already blocked')
            )
            return

        # Add the IP to the blocklist
        try:
            blocked_ip = BlockedIP.objects.create(
                ip_address=ip_address,
                reason=reason
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully blocked IP address: {ip_address}')
            )
            if reason:
                self.stdout.write(f'Reason: {reason}')
        except Exception as e:
            raise CommandError(f'Error blocking IP address: {str(e)}')
