from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.status import HTTP_201_CREATED
from .models import User, Meal, Activity, Progress, Food
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, MealSerializer, ActivitySerializer, ProgressSerializer, RegisterSerializer, FoodSerializer

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MealViewset(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class ActivityViewset(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ProgressViewset(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=HTTP_201_CREATED)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Restrict access

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        })

@api_view(["GET"])
def get_food_list(request):
    """Get a list of all food items"""
    foods = Food.objects.all()
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_food_details(request, food_id, portion_size):
    """Get food details based on portion size"""
    try:
        food = Food.objects.get(id=food_id)
    except Food.DoesNotExist:
        return Response({"error": "Food not found"}, status=404)

    portion_factor = {
        "small": food.portion_small / 100,
        "medium": food.portion_medium / 100,
        "large": food.portion_large / 100,
    }.get(portion_size, 1)

    food_data = {
        "name": food.name,
        "energy_kcal": food.energy_kcal * portion_factor,
        "protein": food.protein * portion_factor,
        "fat": food.fat * portion_factor,
        "carbohydrates": food.carbohydrates * portion_factor,
        "fiber": food.fiber * portion_factor if food.fiber else None,
    }

    return Response(food_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def log_meal(request):
    """Allows users to log a meal by selecting food and portion size."""
    user = request.user
    food_id = request.data.get("food_id")
    portion_size = request.data.get("portion_size")

    try:
        food = Food.objects.get(id=food_id)
    except Food.DoesNotExist:
        return Response({"error": "Food not found"}, status=404)

    # Get portion factor
    portion_factor = {
        "small": food.portion_small / 100,
        "medium": food.portion_medium / 100,
        "large": food.portion_large / 100,
    }.get(portion_size, 1)

    # Calculate meal nutrients
    meal = Meal.objects.create(
        user=user,
        food=food,
        portion_size=portion_size,
        calories=food.energy_kcal * portion_factor,
        protein=food.protein * portion_factor,
        fat=food.fat * portion_factor,
        carbohydrates=food.carbohydrates * portion_factor,
    )

    return Response(MealSerializer(meal).data, status=201)
