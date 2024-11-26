from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from faculties.models import Faculty
from .models import User
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise AuthenticationFailed("Invalid credentials")
        if not user.is_active:
            raise AuthenticationFailed("This account is inactive.")

        # Check if the profile is completed
        if user.is_student:
            from students.models import Student  # Import Student model
            profile_completed = Student.objects.filter(user=user).exists()
        # elif user.is_faculty:
        #     from faculties.models import Faculty  # Import Faculty model
        #     profile_completed = Faculty.objects.filter(user=user).exists()
        else:
            profile_completed = True  

        refresh = RefreshToken.for_user(user)

        return {
            'id': user.pk,
            'username': user.username,
            'is_student': user.is_student,
            'is_faculty': user.is_faculty,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'profile_completed': profile_completed,
        }
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    c_password = serializers.CharField(write_only=True)
    
    class Meta:
        model=get_user_model()
        fields=[
            'username',
            'password',
            'c_password',
            'is_student',
            'is_faculty',
        ]
    def validate(self,value):
        if value['password'] != value['c_password']:
            raise serializers.ValidationError('Passwords do not match.')
        if get_user_model().objects.filter(username=value['username']).exists():
            raise serializers.ValidationError('Username already exists!')
        return value
    
    def create(self,validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_student=validated_data.get('is_student', True),
            is_faculty=validated_data.get('is_faculty', False)
        )
        return user



class FacultyRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    c_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'name','password', 'c_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['c_password']:
            raise serializers.ValidationError('Passwords do not match.')
        if get_user_model().objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError('Username already exists.')
        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
            password=validated_data['password'],
            is_faculty=True,
            is_student=False
        )
        Faculty.objects.create(user=user)
        return user