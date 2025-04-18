from django.urls import path
from .views import RegisterView, UserProfileUpdateView, UserProfileView, get_food_details, get_food_list, log_meal
from .views import CustomTokenObtainPairView  # Custom view for both email login and remember me functionality
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path("food/", get_food_list, name="get_food_list"),
    path("food/<int:food_id>/<str:portion_size>/", get_food_details, name="get_food_details"),
    path("meal/log/", log_meal, name="log_meal"),

    # Custom login with email + Remember Me functionality
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),  # This will handle both
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
