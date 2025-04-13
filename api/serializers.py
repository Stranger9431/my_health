from rest_framework import serializers
from .models import User, Meal, Progress, Activity, Food

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'weight', 'height', 'age',
            'gender', 'pref_diet', 'waist_circ', 'hip_circ', 'goal',
            'activity_level'
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
    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['age', 'weight', 'height', 'gender', 'pref_diet', 'waist_circ', 'hip_circ', 'goal']  # Fields that are updatable

    def update(self, instance, validated_data):
        # Update the instance with the validated data and return it
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance