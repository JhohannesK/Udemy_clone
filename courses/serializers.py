from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Course
from users.serializers import UserSerializer

class CourseDisplaySerializer(ModelSerializer):
    student_no = serializers.IntegerField(source = 'get_enrolled_users')
    author = UserSerializer()
    image_url = serializers.CharField(source='get_absolute_url')
    
    class Meta:
        model = Course
        fields = [
            'course_uuid', 
            'title', 
            'student_no',
            'author',
            'price', 
            'image_url'
        ]