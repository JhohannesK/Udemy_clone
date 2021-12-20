from django.urls import path

from courses.views import CourseHomeView

urlpatterns = [
    path('', CourseHomeView.as_view())
]
