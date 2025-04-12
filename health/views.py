from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import User, Activity, Meal
from .utils import (
    calculate_bmi, classify_bmi, calculate_lean_body_mass, calculate_bmr,
    calculate_met_score, calculate_calories_burned, classify_activity_level,
    calculate_whr, classify_whr, calculate_tee, calculate_tef, calculate_tea
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_health_metrics(request):
    """Fetch user data and return calculated health metrics."""
    user_profile = request.user
    user_activity = Activity.objects.filter(user=request.user).first()  # Avoid error if no activity exists

    # Get user data
    weight = user_profile.weight
    height = user_profile.height
    gender = user_profile.gender
    waist = user_profile.waist_circ
    hip = user_profile.hip_circ

    # Get today's logged meals
    from django.utils.timezone import now
    today_meals = Meal.objects.filter(user=user_profile, timestamp__date=now().date())
    
    # Calculate total daily calorie intake
    total_calories = sum(meal.calories for meal in today_meals)

    # Handle missing activity data
    duration = user_activity.duration if user_activity else 0  # Default to 0 if no activity
    intensity = user_activity.intensity if user_activity else "moderate"

    # Perform calculations
    bmi = calculate_bmi(weight, height)
    bmi_category = classify_bmi(bmi)
    lbm = calculate_lean_body_mass(weight, height, gender)
    bmr = calculate_bmr(lbm)
    met_score = calculate_met_score(weight, duration, intensity)
    calories_burned = calculate_calories_burned(met_score, duration, weight)
    activity_level = classify_activity_level(met_score * duration)
    whr = calculate_whr(waist, hip)
    whr_category = classify_whr(waist, hip, gender)
    tea = calculate_tea(met_score, weight)
    tef = calculate_tef(bmr + tea)
    tee = calculate_tee(bmr, tea, tef)

    return Response({
        "BMI": bmi,
        "BMI Category": bmi_category,
        "Lean Body Mass": lbm,
        "BMR": bmr,
        "MET Score": met_score,
        "Calories Burned": calories_burned,
        "Activity Level": activity_level,
        "WHR": whr,
        "WHR Risk Category": whr_category,
        "TEA": tea,
        "TEF": tef,
        "TEE": tee,
        "Total calories consumed today": total_calories,
    })