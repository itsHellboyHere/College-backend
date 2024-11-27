from django.shortcuts import render
from rest_framework import generics , status
from .serializers import LoginSerializer,RegisterSerializer,FacultyRegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class LoginCreateApiView(
    generics.CreateAPIView
):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=400)
login_create_view=LoginCreateApiView.as_view()

class RegisterCreateApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class=RegisterSerializer


    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data['is_student'] = True
        validated_data['is_faculty'] = False
        user=serializer.save()
     
    def create(self, request, *args, **kwargs):
       
        super().create(request, *args, **kwargs)

        return Response(
            {'message': 'User registered successfully!'},
            status=status.HTTP_201_CREATED
        )
 
register_create_view=RegisterCreateApiView.as_view()

class RegisterFacultyView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = FacultyRegisterSerializer
    
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data['is_student'] = False
        validated_data['is_faculty'] = True
        user=serializer.save()
        
        print({
            'id': user.id,
            'username': user.username,
            'is_student': user.is_student,
            'is_faculty': user.is_faculty,
            'message': 'Faculty registered successfully!'
        })
        message="Faculty registered successfully!"
        return Response({
            
            'id': user.id,
            'username': user.username,
            'is_student': user.is_student,
            'is_faculty': user.is_faculty,
            
        })

register_faculty_view=RegisterFacultyView.as_view()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
      
        return Response({"message": "User logged out successfully!"}, status=200)

logout_view = LogoutView.as_view()