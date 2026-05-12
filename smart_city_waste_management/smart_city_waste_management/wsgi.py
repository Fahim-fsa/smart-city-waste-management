import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_city_waste_management.settings')
application = get_wsgi_application()
