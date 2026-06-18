from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/latest/', views.api_latest_data, name='api_latest'),
    path('api/history/', views.api_history_data, name='api_history'),
]
