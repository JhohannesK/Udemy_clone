from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from courses.models import Course


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self._create_user(email, password, **other_fields)


    def _create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('You must provide a valid email.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        
        user.password = make_password(password)
        user.save()
        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    paid_courses = models.ManyToManyField(Course)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.name
    
    def get_all_courses(self):
        courses = []
        for course in self.paid_courses.all():
            courses.append(course.course_uuid)
        return courses