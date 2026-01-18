# ALX Backend Security - IP Tracking & Security System

A comprehensive Django application for IP tracking, geolocation analytics, rate limiting, anomaly detection, and API security with full Swagger documentation.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Celery](https://img.shields.io/badge/Celery-5.3-brightgreen.svg)](https://docs.celeryproject.org/)
[![API](https://img.shields.io/badge/API-REST-orange.svg)](https://www.django-rest-framework.org/)

## 🎯 Features

### ✅ Task 0: Basic IP Logging Middleware
- Logs IP address, timestamp, and path of every incoming request
- Stores data in PostgreSQL/SQLite database
- Middleware automatically processes all requests

### ✅ Task 1: IP Blacklisting
- Block requests from blacklisted IPs (returns 403 Forbidden)
- Management command to add IPs to blocklist
- Admin interface for managing blocked IPs

### ✅ Task 2: IP Geolocation Analytics
- Extended request logs with country and city fields
- Automatic geolocation lookup using IP-API
- 24-hour caching to reduce API calls
- Handles local/private IPs gracefully

### ✅ Task 3: Rate Limiting by IP
- Configurable rate limits per endpoint
- 5 requests/minute for anonymous users
- 10 requests/minute for authenticated users
- Custom rate limit error handler

### ✅ Task 4: Anomaly Detection
- Hourly Celery task to detect suspicious activity
- Flags IPs with >100 requests per hour
- Flags multiple attempts to access sensitive paths
- Creates SuspiciousIP records for review

### ✅ Deployment Ready
- Production settings with environment variables
- Render.com deployment configuration
- PythonAnywhere deployment guide
- Celery with RabbitMQ support
- **Public Swagger API Documentation**

## 📚 API Documentation

Once deployed, access comprehensive API documentation:

- **Swagger UI**: `https://your-app.onrender.com/swagger/`
- **ReDoc**: `https://your-app.onrender.com/redoc/`
- **OpenAPI Schema**: `https://your-app.onrender.com/api/schema/`

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/your-username/alx-backend-security.git
cd alx-backend-security
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
python manage.py migrate --settings=settings_prod
python manage.py createsuperuser --settings=settings_prod
```

6. **Collect static files**
```bash
python manage.py collectstatic --no-input --settings=settings_prod
```

7. **Start development server**
```bash
python manage.py runserver --settings=settings_prod
```

8. **Start Celery worker** (in another terminal)
```bash
celery -A celery worker --loglevel=info
```

9. **Start Celery beat** (in another terminal)
```bash
celery -A celery beat --loglevel=info
```

### Access the Application

- **Main App**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/admin/
- **API Stats**: http://localhost:8000/api/stats/

## 🌐 Deployment

### Deploy to Render.com (Recommended)

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

**Quick Deploy:**

1. Push code to GitHub
2. Connect repository to Render
3. Use Blueprint deployment with `render.yaml`
4. Render automatically sets up:
   - Web service (Django + Gunicorn)
   - Celery worker
   - Celery beat scheduler
   - PostgreSQL database
   - Redis instance

**Swagger will be publicly accessible at**: `https://your-app.onrender.com/swagger/`

### Deploy to PythonAnywhere

See [PYTHONANYWHERE_DEPLOY.md](PYTHONANYWHERE_DEPLOY.md) for PythonAnywhere-specific instructions.

**Note**: PythonAnywhere free tier has limitations (no Celery support, no outbound connections).

## 📋 API Endpoints

### Public Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/swagger/` | GET | Swagger API documentation |
| `/redoc/` | GET | ReDoc API documentation |
| `/api/stats/` | GET | System statistics |
| `/api/request-logs/` | GET | List all request logs |
| `/api/blocked-ips/` | GET | List blocked IPs |
| `/api/suspicious-ips/` | GET | List suspicious IPs |

### Admin Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/blocked-ips/` | POST | Add blocked IP | Yes |
| `/api/suspicious-ips/{id}/resolve/` | POST | Mark as resolved | Yes |
| `/admin/` | GET | Django admin panel | Yes |

## 🧪 Testing

### Test Deployment

```bash
python test_deployment.py https://your-app.onrender.com
```

### Manual Testing

**Test IP Tracking:**
```bash
curl https://your-app.onrender.com/
# Check admin to see logged request
```

**Test Rate Limiting:**
```bash
for i in {1..10}; do 
  curl -X POST https://your-app.onrender.com/ip_tracking/login/
done
# Should get 429 after 5 requests
```

**Test API:**
```bash
# Get statistics
curl https://your-app.onrender.com/api/stats/

# List request logs
curl https://your-app.onrender.com/api/request-logs/

# Check if IP is blocked
curl https://your-app.onrender.com/api/blocked-ips/check/192.168.1.1/
```

## 🛠️ Management Commands

### Block an IP Address

```bash
# Block without reason
python manage.py block_ip 192.168.1.100

# Block with reason
python manage.py block_ip 192.168.1.100 --reason "Suspicious activity"
```

## 📊 Models

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

## 🔧 Configuration

### Environment Variables

See [.env.example](.env.example) for all available configuration options.

**Required:**
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (False in production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

**Optional:**
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `CELERY_BROKER_URL`: RabbitMQ/Redis URL for Celery

## 📦 Dependencies

- **Django 4.2+**: Web framework
- **Django REST Framework**: API framework
- **drf-spectacular**: Swagger/OpenAPI documentation
- **Celery 5.3+**: Asynchronous task queue
- **Redis**: Caching and Celery broker
- **RabbitMQ**: Celery message broker (recommended)
- **PostgreSQL**: Production database
- **Gunicorn**: WSGI HTTP server

See [requirements.txt](requirements.txt) for complete list.

## 🗂️ Project Structure

```
alx-backend-security/
├── ip_tracking/              # Main Django app
│   ├── models.py            # Database models
│   ├── middleware.py        # IP tracking middleware
│   ├── views.py             # Web views
│   ├── api_views.py         # REST API views
│   ├── serializers.py       # DRF serializers
│   ├── tasks.py             # Celery tasks
│   ├── admin.py             # Admin configuration
│   └── management/
│       └── commands/
│           └── block_ip.py  # Management command
├── settings_prod.py         # Production settings
├── urls.py                  # URL configuration
├── wsgi.py                  # WSGI application
├── celery.py                # Celery configuration
├── requirements.txt         # Python dependencies
├── render.yaml              # Render deployment config
├── Procfile                 # Process definitions
├── runtime.txt              # Python version
└── DEPLOYMENT.md            # Deployment guide
```

## 🔐 Security Features

- ✅ IP-based rate limiting
- ✅ IP blacklisting
- ✅ Anomaly detection
- ✅ HTTPS enforced in production
- ✅ Secure cookies
- ✅ CSRF protection
- ✅ XSS protection
- ✅ Security headers
- ✅ SQL injection protection (Django ORM)

## 📈 Monitoring

### Celery Tasks

- **detect_anomalies**: Runs hourly to flag suspicious IPs
- **cleanup_old_logs**: Optional task to clean old logs

### Admin Dashboard

Access at `/admin/` to:
- View all request logs with geolocation
- Manage blocked IPs
- Review suspicious IP flags
- Monitor system activity

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is part of the ALX Backend Security curriculum.

## 👥 Authors

ALX Backend Security Team

## 🆘 Support

For issues and questions:
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
- Check [PYTHONANYWHERE_DEPLOY.md](PYTHONANYWHERE_DEPLOY.md) for PythonAnywhere
- Review API documentation at `/swagger/`

## 🎓 ALX Project

**Repository**: alx-backend-security  
**Directory**: ip_tracking

---

**Live Demo**: [https://your-app.onrender.com](https://your-app.onrender.com)  
**API Documentation**: [https://your-app.onrender.com/swagger/](https://your-app.onrender.com/swagger/)
