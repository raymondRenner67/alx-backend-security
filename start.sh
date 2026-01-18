#!/bin/bash
# Quick Start Script for Local Development

echo "====================================="
echo "ALX Backend Security - Quick Start"
echo "====================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env with your configuration${NC}"
fi

# Create logs directory
mkdir -p logs

# Run migrations
echo -e "${GREEN}Running migrations...${NC}"
export DJANGO_SETTINGS_MODULE=settings_prod
python manage.py migrate

# Create superuser if needed
echo -e "${YELLOW}Do you want to create a superuser? (y/n)${NC}"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

# Collect static files
echo -e "${GREEN}Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Print instructions
echo ""
echo "====================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "====================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Terminal 1 - Django Server:"
echo "   python manage.py runserver --settings=settings_prod"
echo ""
echo "2. Terminal 2 - Celery Worker:"
echo "   celery -A celery worker --loglevel=info"
echo ""
echo "3. Terminal 3 - Celery Beat:"
echo "   celery -A celery beat --loglevel=info"
echo ""
echo "Access the application:"
echo "  - Main app: http://localhost:8000"
echo "  - Swagger: http://localhost:8000/swagger/"
echo "  - Admin: http://localhost:8000/admin/"
echo ""
echo "====================================="
