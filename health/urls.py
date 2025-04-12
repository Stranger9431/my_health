from django.urls import path
from .views import get_health_metrics

app_name = 'health'

urlpatterns = [
    path('metrics/', get_health_metrics, name='get_health_metrics'),
]