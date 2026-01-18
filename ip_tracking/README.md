# IP Tracking Backend Security

A comprehensive Django application for IP tracking, geolocation, rate limiting, and anomaly detection.

## Features

### Task 0: Basic IP Logging Middleware ✅
- Logs IP address, timestamp, and path of every incoming request
- Stores data in `RequestLog` model
- Middleware registered in settings.py

### Task 1: IP Blacklisting ✅
- Block requests from blacklisted IPs
- Returns 403 Forbidden for blocked IPs
- Management command to add IPs to blocklist
- Admin interface for managing blocked IPs

### Task 2: IP Geolocation Analytics ✅
- Extended `RequestLog` with country and city fields
- Automatic geolocation lookup using ip-api.com
- 24-hour caching to reduce API calls
- Handles local/private IPs gracefully

### Task 3: Rate Limiting by IP ✅
- Configured rate limits:
  - 5 requests/minute for anonymous users
  - 10 requests/minute for authenticated users
- Applied to login and sensitive views
- Custom rate limit error handler

### Task 4: Anomaly Detection ✅
- Hourly Celery task to detect suspicious activity
- Flags IPs with:
  - More than 100 requests per hour
  - Multiple attempts to access sensitive paths (/admin, /login)
- Creates `SuspiciousIP` records for review
- Admin interface with resolution tracking

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install and start Redis (required for Celery):
```bash
# On Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# On macOS
brew install redis
brew services start redis

# On Windows
# Download from https://github.com/microsoftarchive/redis/releases
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

## Usage

### Starting the Application

1. Start Django development server:
```bash
python manage.py runserver
```

2. Start Celery worker:
```bash
celery -A celery worker --loglevel=info
```

3. Start Celery beat (for scheduled tasks):
```bash
celery -A celery beat --loglevel=info
```

### Blocking an IP Address

```bash
# Block an IP
python manage.py block_ip 192.168.1.100

# Block an IP with a reason
python manage.py block_ip 192.168.1.100 --reason "Suspicious activity detected"
```

### Managing Data via Admin

Access the Django admin at `http://localhost:8000/admin/` to:
- View request logs with geolocation data
- Manage blocked IPs
- Review and resolve suspicious IP flags

### Testing Rate Limiting

Visit `http://localhost:8000/ip_tracking/login/` and attempt to login multiple times to test rate limiting.

## Configuration

### settings.py

Key configuration sections:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'ip_tracking',
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    ...
    'ip_tracking.middleware.IPTrackingMiddleware',
]

# Cache configuration (for geolocation caching)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Rate limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Celery Beat schedule
CELERY_BEAT_SCHEDULE = {
    'detect-anomalies-hourly': {
        'task': 'ip_tracking.tasks.detect_anomalies',
        'schedule': crontab(minute=0),  # Every hour
    },
}
```

## Models

### RequestLog
- `ip_address`: IP address of the client
- `timestamp`: When the request was made
- `path`: URL path accessed
- `country`: Country from geolocation (optional)
- `city`: City from geolocation (optional)

### BlockedIP
- `ip_address`: Blocked IP address (unique)
- `reason`: Reason for blocking
- `blocked_at`: When the IP was blocked

### SuspiciousIP
- `ip_address`: Flagged IP address
- `reason`: Why it was flagged
- `flagged_at`: When it was flagged
- `resolved`: Whether the issue has been reviewed

## API Endpoints

- `/ip_tracking/login/` - Rate-limited login view
- `/ip_tracking/api/sensitive/` - Example rate-limited API endpoint

## Celery Tasks

### detect_anomalies
- Runs: Every hour
- Purpose: Flag suspicious IPs
- Criteria:
  - More than 100 requests per hour
  - 5+ attempts to access sensitive paths

### cleanup_old_logs (optional)
- Purpose: Remove old request logs
- Default: Logs older than 30 days

Run manually:
```bash
python manage.py shell
>>> from ip_tracking.tasks import cleanup_old_logs
>>> cleanup_old_logs.delay(days=30)
```

## Security Considerations

1. **Production Geolocation**: Replace ip-api.com with a production-grade service (MaxMind, IPStack, etc.)
2. **Redis Security**: Secure your Redis instance in production
3. **Secret Key**: Change `SECRET_KEY` in settings.py
4. **Debug Mode**: Set `DEBUG = False` in production
5. **ALLOWED_HOSTS**: Configure properly for production

## Testing

Test the middleware:
```python
# Make requests and check logs
curl http://localhost:8000/

# Check admin to see logged requests with geolocation
```

Test rate limiting:
```bash
# Will be rate limited after 5 requests in a minute
for i in {1..10}; do curl -X POST http://localhost:8000/ip_tracking/login/; done
```

## Troubleshooting

### Geolocation not working
- Check internet connectivity
- Verify ip-api.com is accessible
- Check logs for errors

### Rate limiting not working
- Ensure cache is configured
- Check RATELIMIT_ENABLE is True
- Verify middleware order in settings

### Celery tasks not running
- Ensure Redis is running
- Check Celery worker is started
- Check Celery beat is started for scheduled tasks

## License

This project is part of the ALX Backend Security curriculum.

## Repository

- GitHub: alx-backend-security
- Directory: ip_tracking
