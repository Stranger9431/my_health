from django.urls import path
from .views import RegisterView, UserProfileView, get_food_details, get_food_list, log_meal

app_name = 'api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path("food/", get_food_list, name="get_food_list"),
    path("food/<int:food_id>/<str:portion_size>/", get_food_details, name="get_food_details"),
    path("meal/log/", log_meal, name="log_meal")
]