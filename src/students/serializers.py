from rest_framework import serializers

from faculties.models import Faculty
from .models import Student
from subjects.models import Subject

class FacultySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True) 
    class Meta:
        model = Faculty
        fields = ['id','username'] 
        
class SubjectSerializer(serializers.ModelSerializer):
    faculty=FacultySerializer()
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description','faculty']

class StudentSerializer(serializers.ModelSerializer):

    subjects = SubjectSerializer(many=True,required=False)
    class Meta:
        model=Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'blood_group',
            'contact_number',
            'address',
            'subjects'
            # 'profile_pic',
            # 'profile_pic_url',
             # Read-only field for the profile picture URL
        ]
        # read_only_fields = ['profile_pic_url'] 
    
    
class StudentProfilePicUpdateSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False, allow_null=True)
    profile_pic_url=serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ['profile_pic',
                  'profile_pic_url'
                  ]  # Only include the profile_pic field in the serializer
    def get_profile_pic_url(self,obj):
        request=self.context.get('request')
        if obj.profile_pic:
            return request.build_absolute_uri(obj.profile_pic.url)
        return None

