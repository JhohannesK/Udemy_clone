from django.contrib import admin
from .models import Course, Episode, CourseSection, Comment, Sector

# Register your models here.
admin.site.register(Course)
admin.site.register(Episode)
admin.site.register(CourseSection)
admin.site.register(Comment)
admin.site.register(Sector)

