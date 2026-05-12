from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('users/', include('users_app.urls')),
    path('reports/', include('citizen_reports_app.urls')),
    path('tasks/', include('waste_management_app.urls')),
    path('notifications/', include('notifications_app.urls')),
    path('analytics/', include('analytics_app.urls')),
    path('dashboard/', include('users_app.dashboard_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
