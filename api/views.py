from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import viewsets, generics, permissions
from rest_framework.status import HTTP_201_CREATED
from .models import User, Meal, Activity, Progress, Food, Tip, ActivityLog, StepLog, WaterLog
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from datetime import timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import UserSerializer, WaterLogSerializer, WaterHistorySerializer, WaterEntrySerializer, CustomFoodSerializer, ActivityLogSerializer, StepLogSerializer, MealSerializer, TipSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer, ActivitySerializer, ProgressSerializer, RegisterSerializer, FoodSerializer, UserProfileSerializer, UserProfileUpdateSerializer

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MealViewset(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['timestamp']

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)


class ActivityViewset(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ProgressViewset(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_water(request):
    serializer = WaterLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def water_history(request):
    user = request.user
    date_str = request.GET.get('date')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if date_str:
        date = parse_date(date_str)
        logs = WaterLog.objects.filter(user=user, date_logged=date)
        total = sum(log.amount for log in logs)
        response_data = {
            "date": date,
            "total_water": total,
            "target_water": user.daily_water_goal or 2.5,
            "entries": WaterEntrySerializer(logs, many=True).data
        }
        return Response(response_data)

    elif start_date_str and end_date_str:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        history = []
        current_date = start_date
        while current_date <= end_date:
            logs = WaterLog.objects.filter(user=user, date_logged=current_date)
            total = sum(log.amount for log in logs)
            history.append({
                "date": current_date,
                "total_water": total,
                "target_water": user.daily_water_goal or 2.5,
                "entries": WaterEntrySerializer(logs, many=True).data
            })
            current_date += timedelta(days=1)
        return Response(history)

    else:
        return Response({"error": "Provide either 'date' or both 'start_date' and 'end_date' in YYYY-MM-DD format."}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_custom_food(request):
    required_fields = ['name', 'energy_kcal', 'protein', 'fat', 'carbohydrates']
    for field in required_fields:
        if field not in request.data:
            return Response({field: "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CustomFoodSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def create_superuser_view(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='stranger',
            email='stranger@example.com',
            password='TobiPass123!'
        )
        return JsonResponse({"message": "Superuser created"})
    else:
        return JsonResponse({"message": "Superuser already exists"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meal_summary(request):
    date_str = request.GET.get('date')
    if date_str:
        parsed_date = parse_date(date_str)
        if not parsed_date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
    else:
        parsed_date = now().date()

    meals = Meal.objects.filter(user=request.user, timestamp__date=parsed_date)

    total_calories = sum(meal.calories for meal in meals)
    total_protein = sum(meal.protein or 0 for meal in meals)
    total_carbs = sum(meal.carbohydrates or 0 for meal in meals)
    total_fat = sum(meal.fat or 0 for meal in meals)

    return Response({
        "date": parsed_date,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbohydrates": total_carbs,
        "total_fat": total_fat
    })

class MealUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, meal_id):
        meal = get_object_or_404(Meal, id=meal_id, user=request.user)

        serializer = MealSerializer(meal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Meal updated successfully.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MealDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, meal_id):
        meal = get_object_or_404(Meal, id=meal_id, user=request.user)
        meal.delete()
        return Response({'message': 'Meal deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=HTTP_201_CREATED)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    
class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can update their profile

    def put(self, request, *args, **kwargs):
        return self._update(request)

    def patch(self, request, *args, **kwargs):
        return self._update(request)

    def _update(self, request):
        # Get the authenticated user
        user = request.user

        # Initialize the serializer with the user instance, request data, and any uploaded files
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)

        # Log the received data and check if the serializer is valid
        print("Received data:", request.data)  # Debugging line
        print("Is serializer valid?", serializer.is_valid())  # Debugging line

        if serializer.is_valid():
            # Save the data
            serializer.save()
            # Return the updated user profile data
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If validation fails, return the error messages
        print("Serializer errors:", serializer.errors)  # Debugging line
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Get the email and password from the request data
        email = request.data.get('email')  # Expecting email for login
        password = request.data.get('password')
        remember_me = request.data.get('remember_me', False)  # Get the remember_me flag
        
        # Default expiration time for access token
        access_token_lifetime = timedelta(minutes=5) 
        
        # Longer expiration for refresh token if "Remember Me" is checked
        refresh_token_lifetime = timedelta(days=1)  # Default: 1 day
        if remember_me:
            refresh_token_lifetime = timedelta(days=30)  # Extend refresh token expiration to 30 days

        # Authenticate user using email
        user = authenticate(request, username=email, password=password)

        # If user is authenticated, generate tokens
        if user is not None:
            # Create JWT access and refresh tokens
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == status.HTTP_200_OK:
                # Generate custom refresh token with custom expiration time
                refresh_token = RefreshToken.for_user(user)
                refresh_token.set_exp(lifetime=refresh_token_lifetime)  # Set custom expiration time for refresh token
                
                # Add the refresh token to the response
                response.data['refresh'] = str(refresh_token)
            
            return response
        else:
            return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        

class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        # Construct reset URL (you'd ideally have a frontend to handle this)
        reset_url = f"{settings.FRONTEND_BASE_URL}/reset-password?uidb64={uidb64}&token={token}"

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "We’ve emailed you instructions for setting your password."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    

class LogActivityView(generics.CreateAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LogStepsView(generics.CreateAPIView):
    serializer_class = StepLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityHistoryView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivityLog.objects.filter(user=self.request.user).order_by('-date', '-time')

class StepHistoryView(generics.ListAPIView):
    serializer_class = StepLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StepLog.objects.filter(user=self.request.user).order_by('-date', '-time')


@api_view(["GET"])
def get_all_tips(request):
    tips = Tip.objects.all()
    serializer = TipSerializer(tips, many=True)
    return Response(serializer.data)