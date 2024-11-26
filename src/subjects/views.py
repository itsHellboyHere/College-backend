from django.shortcuts import render
from rest_framework import generics

from faculties.models import Faculty
from .models import Subject
from .serializers import SubjectSerializer
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsFacultyPermission
from rest_framework.response import Response
from rest_framework import status
from students.models import Student
from authentication.models import User
class SubjectCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsFacultyPermission]
    serializer_class = SubjectSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user

        try:
            # Try to get the faculty associated with the user
            faculty = Faculty.objects.get(user=user)
        except Faculty.DoesNotExist:
            # If no Faculty record is found, return a 403 error
            return Response(
                {'detail': 'User is not associated with any faculty.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Add the faculty to the request data before serialization
        request.data['faculty'] = faculty.id

        # Serialize the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the subject and associate it with the faculty
        subject = serializer.save(faculty=faculty)

        return Response({
            'message': 'Subject created successfully!',
            'subject': serializer.data,
            'faculty_name': faculty.user.name  # Get faculty name
        }, status=status.HTTP_201_CREATED)

# This will be the view to handle subject creation
create_subject_view = SubjectCreateView.as_view()

class AssignSubjectToStudentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsFacultyPermission]

    def post(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            subject_id = request.data['subject_id']
            subject = Subject.objects.get(id=subject_id)
        except (Student.DoesNotExist, Subject.DoesNotExist):
            return Response({"detail": "Student or Subject not found."}, status=status.HTTP_400_BAD_REQUEST)

        student.subjects.add(subject)  
        return Response({"message": "Subject assigned to student successfully."}, status=status.HTTP_200_OK)
    
assign_subject_to_student=AssignSubjectToStudentView.as_view()
