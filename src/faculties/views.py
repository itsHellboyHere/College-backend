from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from faculties.models import Faculty
from students.models import Student
from students.serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsFacultyPermission
from django.utils.crypto import get_random_string
from authentication.models import User
from rest_framework.exceptions import NotFound
from rest_framework import serializers
from students.serializers import StudentSerializer
from api.permissions import IsFacultyPermission,IsStudentPermission
# Create your views here.
class ViewAllStudentsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

list_view_all_student=ViewAllStudentsView.as_view()
class FacultyCreateStudentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsFacultyPermission]
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        # Create User for the Student
        username = serializer.validated_data['first_name'].lower() + get_random_string(5)
        password = get_random_string(8)
        user = User.objects.create_user(
            username=username,
            password=password,
            is_student=True
        )
        
     
        student = serializer.save(user=user)
    
        faculty = Faculty.objects.get(user=self.request.user)  
        faculty.students.add(student)  
    
faculty_create_student_view = FacultyCreateStudentView.as_view()



class SingleStudentView(generics.RetrieveAPIView):
    
    permission_classes = [IsAuthenticated, IsFacultyPermission]
    serializer_class = StudentSerializer

    def get_queryset(self):
       
        faculty = Faculty.objects.get(user=self.request.user)
        return faculty.students.all()

    def get_object(self):
       
        try:
            return self.get_queryset().get(pk=self.kwargs['id'])
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")
get_single_student_view=SingleStudentView.as_view()


class StudentDetailView(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated,IsFacultyPermission]
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
