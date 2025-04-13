from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        # Override to use email instead of username
        self.user = authenticate(
            request=self.context.get('request'),
            username=attrs.get("email"),
            password=attrs.get("password")
        )

        if not self.user:
            raise serializers.ValidationError("Invalid credentials.")

        data = super().validate(attrs)
        data['user'] = {
            "id": self.user.id,
            "email": self.user.email,
            "username": self.user.username,
        }
        return data

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
