from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework import generics,status
from rest_framework.response import Response
from faculties.models import Faculty
from students.models import Student
from students.serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsFacultyPermission
from django.utils.crypto import get_random_string
from authentication.models import User
from rest_framework.exceptions import NotFound,ValidationError
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
       
        username = serializer.validated_data['first_name'].lower() + get_random_string(5)
        password = get_random_string(8)
        email=self.request.data.get('email',None)
        if not email:
            raise ValidationError({"email": "Email is required."})
        user = User.objects.create_user(
            username=username,
            password=password,
            is_student=True
        )
        
     
        student = serializer.save(user=user)
        faculty = Faculty.objects.get(user=self.request.user)  
        faculty.students.add(student)  
        subject = "Welcome to the University"
        message = (
            f"Dear {serializer.validated_data['first_name']},\n\n"
            f"Your student account has been created successfully. Below are your login details:\n\n"
            f"Username: {username}\n"
            f"Password: {password}\n\n"
            f"Please log in.\n\n"
            f"Best regards,\nThe University Team"
        )
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER, 
            [email], 
            fail_silently=False,  
        )
        return student
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = self.perform_create(serializer)

 
        response_data = {
            "message": f"Student '{serializer.validated_data['first_name']}' was created successfully.",
            "email": request.data.get('email'),
            "student_id": student.id,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
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
