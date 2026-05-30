from rest_framework import serializers
from django.contrib.auth.models import User
from .models import APIKEY
import re
def error_password(value):
    if len(value)<8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    elif not any(char.islower() for char in value):
        raise serializers.ValidationError("Password must contain at least one lowercase letter (a-z).")
    elif not any(char.isupper() for char in value):
        raise serializers.ValidationError("Password must contain at least one uppercase letter (A-Z).")
    elif not any(char.isdigit() for char in value):
        raise serializers.ValidationError("Password must contain at least one digit (0-9).")
    elif not any(not char.isalnum() for char in value):
        raise serializers.ValidationError("Password must contain at least one special character (e.g., @, #, $, %, &).")

def username_error(value):
    if len(value)<5:
        raise serializers.ValidationError("Username must be at least 5 characters long.")
    elif value[0].isdigit():
        raise serializers.ValidationError("Username cannot start with a number.")
    elif not re.fullmatch(r'^[a-zA-Z0-9._]+$',value):
        raise serializers.ValidationError("Username can only contain letters, numbers, underscores (_), and periods (.).")
    return value.lower()
class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,validators=[error_password])
    username=serializers.CharField(validators=[username_error])
    email=serializers.EmailField(required=True)
    class Meta:
        model=User
        fields=['username','password','email']
    def validate(self,data):
        username=data.get('username')
        email=data.get('email')
        errors = {}
        if User.objects.filter(username=username).exists():
            errors['username'] = ['This username is not available.']
        if User.objects.filter(email=email).exists():
            errors['email'] = ['This email is already registered.']
        if errors:
            raise serializers.ValidationError(errors)    
        return data

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

class APIKeySerializername(serializers.Serializer):
    key_name=serializers.CharField(required=True)


def name_error(value):
    if not re.fullmatch(r'^[A-Za-z ]+$',value):
        raise serializers.ValidationError("Company name looks invalid. Only alphabetical letters (A-Z) and spaces are allowed.")
class UserProfileSerializer(serializers.Serializer):
    company_name=serializers.CharField(required=True,validators=[name_error])        


class APIKeySerializers(serializers.ModelSerializer):
    class Meta:
        model=APIKEY
        fields=['id','key_name','is_active','created_at']
    