from django.db import models
from authentication.models import User
# from subjects.models import Subject
# from students.models import Student
# Create your models here.
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    students = models.ManyToManyField('students.Student', related_name='faculties', blank=True)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='faculties', null=True)
    def __str__(self):
        return self.user.username