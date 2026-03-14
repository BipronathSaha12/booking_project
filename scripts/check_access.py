import os, sys
import django

# Ensure both the Django project package directory and the project root are on Python path
PROJECT_PKG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
for p in (PROJECT_PKG_DIR, PROJECT_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpass')
    user.save()
    print('Created testuser')
else:
    print('testuser exists')

client = Client()
print('GET /dashboard (not logged in) ->', client.get('/dashboard/').status_code)
print('GET /service/1 (not logged in) ->', client.get('/service/1/').status_code)

client.login(username='testuser', password='testpass')
print('Logged in status ->', client.login(username='testuser', password='testpass'))
print('GET /dashboard (logged in) ->', client.get('/dashboard/').status_code)
print('GET /service/1 (logged in) ->', client.get('/service/1/').status_code)
