from django.shortcuts import render
from rest_framework.views import APIView
from .models import Student
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import StudentSerializer,StudentProfilePicUpdateSerializer,SubjectSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsStudentPermission
from rest_framework_simplejwt.authentication import JWTAuthentication 
from subjects.models import Subject
# Create your views here.





class StudentDetailCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsStudentPermission]
    serializer_class = StudentSerializer
    def get_object(self):
      
        try:
            return self.request.user.student_profile
        except Student.DoesNotExist:
            raise Response(
                {'error': 'Student profile not found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_student:
            raise serializers.ValidationError({'error': 'Only students can add their details.'})

        if hasattr(user, 'student_profile'):
            raise serializers.ValidationError({'error': 'Student details already exist for this user.'})

     
        student = serializer.save(user=user)
        return Response(
            {
                'message': 'Student details added successfully!',
                'id': student.id,  
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

student_detail_create_view = StudentDetailCreateView.as_view()

class StudentDetailView(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated,IsStudentPermission]
    queryset=Student.objects.all()
    lookup_field='id'
    serializer_class=StudentSerializer
    serializer_class = StudentSerializer
    def get_object(self):
        
        try:
            return self.request.user.student_profile
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student details not found for this user.")

student_list_view=StudentDetailView.as_view()

class StudentDetailUpdateView(
    generics.UpdateAPIView
):
    queryset=Student.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class=StudentSerializer

    def get_object(self):
       
        user = self.request.user
        if not hasattr(user, 'student_profile'):
            raise serializers.ValidationError("Student details not found for this user.")
        return user.student_profile 
    


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        response = super().update(request, partial=partial, *args, **kwargs)
        return Response(
            {'message': 'Student details updated successfully!', 'data': response.data},
            status=status.HTTP_200_OK
        )
    
student_detail_update_view = StudentDetailUpdateView.as_view()

class StudentProfilePicUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated,IsStudentPermission]
    serializer_class = StudentProfilePicUpdateSerializer

    def get_object(self):
        
        user = self.request.user
        if not hasattr(user, 'student_profile'):
            raise serializers.ValidationError("Student profile not found for this user.")
        return user.student_profile

    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', True)
        response = super().update(request, partial=partial, *args, **kwargs)
        return Response(
            {
                'message': 'Profile picture updated successfully!',
                'data': response.data
            },
            status=status.HTTP_200_OK
        )
student_profile_pic_update_view=StudentProfilePicUpdateView.as_view()

class StudentSubjectView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,IsStudentPermission]
    serializer_class = SubjectSerializer
    # queryset = Subject.objects.all()
    def get_queryset(self):
        try:
          
            student = self.request.user.student_profile  
            return student.subjects.all()
        except Student.DoesNotExist:
            raise ValidationError("No student profile associated with this user.")

student_subject_view = StudentSubjectView.as_view()

