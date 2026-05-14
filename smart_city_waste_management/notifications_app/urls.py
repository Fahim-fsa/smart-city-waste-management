from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list_view, name='notification_list'),
    path('<int:pk>/', views.notification_detail_view, name='notification_detail'),
    path('mark-all-read/', views.mark_all_read_view, name='mark_all_read'),
]
