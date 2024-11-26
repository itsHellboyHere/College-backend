from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    def clean(self):
        if self.is_student and self.is_faculty:
            raise ValueError("A user cannot be both a student and a teacher.")
    
