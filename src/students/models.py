from django.db import models
from authentication.models import User
from subjects.models import Subject


# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    # print(user)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=10,choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    blood_group=models.CharField(max_length=3,choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    contact_number=models.CharField(max_length=13);
    address=models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True) 
    subjects = models.ManyToManyField(Subject, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"