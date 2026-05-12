from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list_view, name='report_list'),
    path('new/', views.report_form_view, name='report_form'),
    path('<int:pk>/', views.report_detail_view, name='report_detail'),
    path('history/', views.report_history_view, name='report_history'),
    path('<int:pk>/approve/', views.report_approve_view, name='report_approve'),
    path('<int:pk>/reject/', views.report_reject_view, name='report_reject'),
]
