from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('new/', views.task_form_view, name='task_form'),
    path('<int:pk>/', views.task_detail_view, name='task_detail'),
    path('history/', views.task_history_view, name='task_history'),
]
