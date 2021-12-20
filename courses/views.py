from os import statvfs_result
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.models import Sector
from .serializers import CourseDisplaySerializer


class CourseHomeView(APIView):
    
    def get(self, request, *args, **kwargs):
        sectors = Sector.objects.order_by('?')[:6]
        
        sector_response = []
        
        for sector in sectors:
            sector_courses = sector.related_courses.order_by('?')[:4]
            course_serializer = CourseDisplaySerializer(sector_courses, many=True)
            
            sector_obj = {
                'sector_name': sector.sector_name,
                'sector_uuid': sector.sector_uuid,
                'featured_courses': course_serializer.data, 
                'sector_image': sector.get_absolute_url_of_image()
            }
            
            sector_response.append(sector_obj)
            
        return Response(data=sector_response, status=status.HTTP_200_OK)