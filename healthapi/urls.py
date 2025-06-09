from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from api.views import UserViewset, MealViewset, ActivityViewset, ProgressViewset
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Custom API Root View
@api_view(['GET'])
def custom_api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'meals': reverse('meal-list', request=request, format=format),
        'activities': reverse('activity-list', request=request, format=format),
        'progress': reverse('progress-list', request=request, format=format),
        'register': reverse('register', request=request, format=format),
        'profile': reverse('profile', request=request, format=format),
        'update_profile': reverse('profile_update', request=request, format=format),
        'food_list': reverse('get_food_list', request=request, format=format),
        'create_custom_food': reverse('create_custom_food', request=request, format=format),
        'log_meal': reverse('log_meal', request=request, format=format),
        'meal_summary': reverse('meal_summary', request=request, format=format),
        'meal_update': reverse('meal_update', request=request, format=format),
        'meal_delete': reverse('meal_delete', request=request, format=format),
        'log_water': reverse('log_water', request=request, format=format),
        'log_activity': reverse('log_activity', request=request, format=format),
        'log_steps': reverse('log_steps', request=request, format=format),
        'water_history': reverse('water_history', request=request, format=format),
        'activity_history': reverse('activity_history', request=request, format=format),
        'steps_history': reverse('steps_history', request=request, format=format),
        'tips': reverse('get-all-tips', request=request, format=format),
        'password_reset_request': reverse('password_reset_request', request=request, format=format),
        'password_reset_confirm': reverse('password_reset_confirm', request=request, format=format),
        'token': reverse('token_obtain_pair', request=request, format=format),
        'token_refresh': reverse('token_refresh', request=request, format=format),
        'health_metrics': reverse('health:get_health_metrics', request=request, format=format),
    })


# DRF router for viewsets
router = DefaultRouter()
router.register('users', UserViewset)
router.register('meals', MealViewset, basename='meal')
router.register('activities', ActivityViewset)
router.register('progress', ProgressViewset)

# Use custom root view name
router.root_view_name = 'custom-api-root'

urlpatterns = [
    path('', custom_api_root, name='custom-api-root'),  # Custom API root
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # DRF router URLs
    path('api/', include('api.urls')),  # Your custom API paths
    path('health/', include('health.urls')),  # Health metrics
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
