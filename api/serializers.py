from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from .models import User, Meal, Progress, Activity, Food, Tip

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'weight', 'height', 'age',
            'gender', 'pref_diet', 'waist_circ', 'hip_circ', 'goal',
            'activity_level', 'image',
            'daily_water_goal', 'weekly_activity_goal', 'weight_goal', 'daily_steps_goal'
        ]

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'type', 'duration', 'intensity', 'step_count', 'date_logged']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'weight', 'bmi', 'date_logged']

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'weight', 'height', 'age', 'gender', 'pref_diet',
            'waist_circ', 'hip_circ', 'goal', 'activity_level'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "weight",
            "height",
            "age",
            "gender",
            "pref_diet",
            "waist_circ",
            "hip_circ",
            "goal",
            "activity_level",
            "daily_water_goal",
            "weekly_activity_goal",
            "weight_goal",
            "daily_steps_goal",
            "image"
        ]

    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['age', 'weight', 'height', 'gender', 'pref_diet', 'waist_circ', 'hip_circ', 'goal', 'image',
                  'daily_water_goal', 'weekly_activity_goal', 'weight_goal', 'daily_steps_goal'  # NEW
        ]

    def validate_daily_water_goal(self, value):
        if value is not None and value > 5:
            raise serializers.ValidationError("Daily water goal cannot exceed 5 liters.")
        return value

    def validate_weekly_activity_goal(self, value):
        if value is not None and value > 7:
            raise serializers.ValidationError("Weekly activity goal cannot exceed 7 days.")
        return value

    def validate_daily_steps_goal(self, value):
        if value is not None and value > 10000:
            raise serializers.ValidationError("Daily steps goal cannot exceed 10,000 steps.")
        return value

    def update(self, instance, validated_data):
        # Update the instance with the validated data and return it
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email.")
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("The reset link is invalid or has expired.")

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise serializers.ValidationError("The reset link is invalid.", code='invalid_link')
        

class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ['id', 'content']