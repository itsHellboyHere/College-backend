from rest_framework import serializers
from .models import Subject
from faculties.models import Faculty
class SubjectSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField( read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'faculty']
