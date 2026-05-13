from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_dashboard_view, name='analytics_dashboard'),
    path('generate/', views.generate_report_view, name='report_generation'),
]
