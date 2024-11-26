from django.db import models

from faculties.models import Faculty



class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    faculty = models.ForeignKey(
        'faculties.Faculty',  
        on_delete=models.CASCADE,
        related_name='subjects',
        null=True
    )
    def __str__(self):
        return self.name