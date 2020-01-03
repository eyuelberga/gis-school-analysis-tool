from django.views import generic
from django.views.generic import DetailView
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import School

longitude = 38.7494272
latitude = 8.943757
user_location = Point(longitude, latitude, srid=4326)


class Home(generic.ListView):
    model = School
    context_object_name = 'schools'
    template_name = 'schools/dashboard.html'
    queryset = School.objects.all()


class Schools(generic.ListView):
    model = School
    context_object_name = 'schools'
    queryset = School.objects.all()
    template_name = 'schools/schools.html'


class DistanceAnalysis(generic.ListView):
    model = School
    context_object_name = 'schools'
    queryset = School.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[0:6]
    template_name = 'schools/distance_analysis.html'


class SchoolsDetailView(DetailView):
    template_name = 'schools/detail.html'
    model = School
