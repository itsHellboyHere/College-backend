from rest_framework import serializers
from subjects.models import Subject
from .models import Faculty

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description']

class FacultySerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True,required=False)

    class Meta:
        model = Faculty
        fields = ['id', 'user', 'subjects']

