from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator


# Create your models here.
class User(AbstractUser):
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    pref_diet = models.CharField(max_length=50, null=True)
    waist_circ = models.FloatField(null=True, blank=True)
    hip_circ = models.FloatField(null=True, blank=True)
    goal = models.CharField(max_length=100, null=True)
    activity_level = models.CharField(max_length=20, null=True)
    image = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    
    email = models.EmailField(unique=True)  # This ensures email is unique in the database
    daily_water_goal = models.FloatField(null=True, blank=True)  # liters
    weekly_activity_goal = models.IntegerField(null=True, blank=True)  # days
    weight_goal = models.FloatField(null=True, blank=True)  # kg
    target_daily_calories = models.IntegerField(null=True, blank=True)
    daily_steps_goal = models.IntegerField(null=True, blank=True)  # steps
    # Set email as the primary login field
    USERNAME_FIELD = 'email'
    # Optionally define required fields for creating a user via the admin or CLI
    REQUIRED_FIELDS = ['username']  # username is still needed, but won't be used for login

User = get_user_model()

class Food(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Food name
    energy_kcal = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbohydrates = models.FloatField()
    fiber = models.FloatField(null=True, blank=True)
    calcium = models.FloatField(null=True, blank=True)
    iron = models.FloatField(null=True, blank=True)
    magnesium = models.FloatField(null=True, blank=True)
    portion_small = models.FloatField(default=50, null=True, blank=True)
    portion_medium = models.FloatField(default=100, null=True, blank=True)
    portion_large = models.FloatField(default=150, null=True, blank=True) 

    def __str__(self):
        return self.name

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)  # Food item
    portion_size = models.CharField(max_length=10, choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")], null=True, blank=True)
    calories = models.FloatField()  # Automatically calculated
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    carbohydrates = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food.name} ({self.portion_size})"

# class Meal(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     meal_time = models.CharField(max_length=20, null=True)
#     calories = models.FloatField()
#     date_logged = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    duration = models.IntegerField() # in minutes
    intensity = models.CharField(max_length=20, null=True)
    step_count = models.IntegerField(null=True)
    date_logged = models.DateTimeField(auto_now_add=True)

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    bmi = models.FloatField()
    date_logged = models.DateTimeField(auto_now_add=True)


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)  # NEW

    def __str__(self):
        return f"{self.user.email} - {self.activity_type} on {self.date} at {self.time}"

class StepLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)  # NEW

    def __str__(self):
        return f"{self.user.email} - {self.steps} steps on {self.date} at {self.time}"


class WaterLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    date_logged = models.DateField(auto_now_add=True)




class Tip(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:50]  # Short preview
    
