from django.conf import settings
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from decimal import Decimal
from .carry import get_time
from mutagen.mp4 import MP4, MP4StreamInfoError

class Sector(models.Model):
    sector_name = models.CharField(max_length=255)
    sector_uuid = models.UUIDField(default=uuid.uuid5, unique=True)
    related_courses = models.ManyToManyField('Course')
    sector_image = models.ImageField(upload_to='sector_image')
    
    
    def get_absolute_url_of_image(self):
        return 'http://localhost' + self.sector_image
    
    
    
class Course(models.Model):
    title = models.CharField(max_length= 255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    course_section = models.ManyToManyField('CourseSection')
    comments = models.ManyToManyField('Comment')
    image_url = models.ImageField(upload_to='course_images')
    course_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    
    def get_description(self):
        return self.description[:100]
    
    def get_enrolled_users(self):
        enrolled_user = get_user_model().objects.filter(paid_courses=self)
        return len(enrolled_user)
    
    def get_total_episodes(self):
        lessons = 0
        for section in self.course_section:
            lessons += len(section.episodes.all())
        return lessons
    
    def total_course_length(self):
        length = Decimal(0.0)
        for section in self.course_section:
            for episode in section.episodes.all():
                length += episode.length
        return get_time(length, type='short')
    
    
class CourseSection(models.Model):
    section_title=models.CharField(max_length=225,blank=True,null=True)
    section_number=models.IntegerField(blank=True,null=True)
    episodes=models.ManyToManyField('Episode',blank=True)
    
    def total_length(self):
        total = Decimal(0.0)
        for episode in self.episodes.all():
            total += episode.length
            
        return get_time(total, type= 'min')
    
    
class Section(models.Model):
    section_title = models.CharField(max_length=255)
    episodes = models.ManyToManyField('Episode')
    
    
class Episode(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_videos')
    length = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def get_video_length(self):
        try:
            video = MP4(self.file)
        except MP4StreamInfoError
            
    
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    