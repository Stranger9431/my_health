from django.urls import path
from .views import RegisterView, MealDeleteView, MealUpdateView, water_history, log_water, meal_summary, create_custom_food, UserProfileUpdateView, LogActivityView, LogStepsView, ActivityHistoryView, StepHistoryView, RequestPasswordResetView, PasswordResetConfirmView, UserProfileView, get_food_details, get_food_list, log_meal, get_all_tips
from .views import CustomTokenObtainPairView  # Custom view for both email login and remember me functionality
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path("password-reset/request/", RequestPasswordResetView.as_view(), name="password_reset_request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("tips/", get_all_tips, name="get-all-tips"),
    path("food/", get_food_list, name="get_food_list"),
    path("food/<int:food_id>/<str:portion_size>/", get_food_details, name="get_food_details"),
    path("meal/log/", log_meal, name="log_meal"),
    path('meals/<int:meal_id>/update/', MealUpdateView.as_view(), name='meal_update'),
    path('meals/<int:meal_id>/delete/', MealDeleteView.as_view(), name='meal_delete'),
    path("activity/log/", LogActivityView.as_view(), name="log_activity"),
    path("steps/log/", LogStepsView.as_view(), name="log_steps"),
    path("activity/history/", ActivityHistoryView.as_view(), name="activity_history"),
    path("steps/history/", StepHistoryView.as_view(), name="steps_history"),
    path("food/custom/", create_custom_food, name="create_custom_food"),
    path("water/log/", log_water, name="log_water"),
    path('water/history/', water_history, name='water_history'),
    path("meals/summary/", meal_summary, name="meal_summary"),



    # Custom login with email + Remember Me functionality
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),  # This will handle both
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
