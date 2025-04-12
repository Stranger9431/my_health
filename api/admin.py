from django.contrib import admin
from .models import User, Meal, Activity

# Register your models here.
admin.site.register(User)
admin.site.register(Meal)
admin.site.register(Activity)