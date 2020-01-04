from django.views import generic
from django.views.generic import DetailView
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import get_object_or_404
from .models import School

longitude = 38.7494272
latitude = 8.943757


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
    # model = School
    context_object_name = 'schools'
    assessment = True



    def get_queryset(self):
        user_location = Point(float(self.kwargs['lat']), float(self.kwargs['lng']), srid=4326)
        queryset = School.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[0:6]
        self.assessment = queryset[0].distance.km <= 5.0
        return queryset

    template_name = 'schools/distance_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lat'] = self.kwargs['lat']
        context['lng'] = self.kwargs['lng']
        context['assessment'] = self.assessment
        return context


class SchoolsDetailView(DetailView):
    template_name = 'schools/detail.html'
    model = School
