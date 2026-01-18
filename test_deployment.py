#!/usr/bin/env python
"""
Test script for deployed application.
Tests all endpoints including Swagger documentation.

Usage:
    python test_deployment.py https://your-app.onrender.com
"""

import sys
import requests
import json
from time import sleep


def test_swagger(base_url):
    """Test Swagger documentation accessibility"""
    print("\n" + "="*50)
    print("Testing Swagger Documentation")
    print("="*50)
    
    endpoints = [
        '/swagger/',
        '/redoc/',
        '/api/schema/',
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            status = "✅ PASS" if response.status_code == 200 else "❌ FAIL"
            print(f"{status} - {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ FAIL - {endpoint} - Error: {str(e)}")


def test_api_endpoints(base_url):
    """Test API endpoints"""
    print("\n" + "="*50)
    print("Testing API Endpoints")
    print("="*50)
    
    endpoints = [
        ('/api/stats/', 'GET'),
        ('/api/request-logs/', 'GET'),
        ('/api/blocked-ips/', 'GET'),
        ('/api/suspicious-ips/', 'GET'),
    ]
    
    for endpoint, method in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            if method == 'GET':
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, timeout=10)
            
            status = "✅ PASS" if response.status_code in [200, 401, 403] else "❌ FAIL"
            print(f"{status} - {method} {endpoint} - Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   Response keys: {list(data.keys())[:5]}")
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ FAIL - {endpoint} - Error: {str(e)}")


def test_rate_limiting(base_url):
    """Test rate limiting"""
    print("\n" + "="*50)
    print("Testing Rate Limiting")
    print("="*50)
    
    url = f"{base_url}/ip_tracking/login/"
    
    print(f"Sending 10 requests to {url}")
    rate_limited = False
    
    for i in range(10):
        try:
            response = requests.post(
                url,
                data={'username': 'test', 'password': 'test'},
                timeout=5
            )
            
            if response.status_code == 429:
                rate_limited = True
                print(f"✅ Request {i+1}: Rate limited (429)")
                break
            else:
                print(f"   Request {i+1}: Status {response.status_code}")
            
            sleep(0.5)
        except Exception as e:
            print(f"   Request {i+1}: Error - {str(e)}")
    
    if rate_limited:
        print("✅ PASS - Rate limiting is working")
    else:
        print("⚠️  WARNING - Rate limiting may not be active")


def test_ip_tracking(base_url):
    """Test IP tracking"""
    print("\n" + "="*50)
    print("Testing IP Tracking")
    print("="*50)
    
    # Make a request to trigger IP tracking
    try:
        response = requests.get(base_url, timeout=10)
        print(f"✅ Request made - Status: {response.status_code}")
        print("   Check admin panel to verify IP was logged")
        print(f"   Admin: {base_url}/admin/ip_tracking/requestlog/")
    except Exception as e:
        print(f"❌ Error making request: {str(e)}")


def test_admin_panel(base_url):
    """Test admin panel accessibility"""
    print("\n" + "="*50)
    print("Testing Admin Panel")
    print("="*50)
    
    url = f"{base_url}/admin/"
    try:
        response = requests.get(url, timeout=10)
        status = "✅ PASS" if response.status_code in [200, 302] else "❌ FAIL"
        print(f"{status} - Admin panel - Status: {response.status_code}")
        print(f"   URL: {url}")
    except Exception as e:
        print(f"❌ FAIL - Error: {str(e)}")


def test_static_files(base_url):
    """Test static files are being served"""
    print("\n" + "="*50)
    print("Testing Static Files")
    print("="*50)
    
    # Try to access admin static files
    url = f"{base_url}/static/admin/css/base.css"
    try:
        response = requests.get(url, timeout=10)
        status = "✅ PASS" if response.status_code == 200 else "❌ FAIL"
        print(f"{status} - Static files - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ FAIL - Error: {str(e)}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_deployment.py <base_url>")
        print("Example: python test_deployment.py https://your-app.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print("="*50)
    print(f"Testing Deployment: {base_url}")
    print("="*50)
    
    # Run all tests
    test_swagger(base_url)
    test_api_endpoints(base_url)
    test_admin_panel(base_url)
    test_static_files(base_url)
    test_ip_tracking(base_url)
    test_rate_limiting(base_url)
    
    print("\n" + "="*50)
    print("Testing Complete!")
    print("="*50)
    print(f"\n📚 Swagger Documentation: {base_url}/swagger/")
    print(f"📚 ReDoc Documentation: {base_url}/redoc/")
    print(f"⚙️  Admin Panel: {base_url}/admin/")
    print(f"📊 API Stats: {base_url}/api/stats/")


if __name__ == '__main__':
    main()
