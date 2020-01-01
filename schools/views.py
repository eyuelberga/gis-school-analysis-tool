from django.shortcuts import render
from django.views import generic
from django.views.generic import DetailView
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import School
from pathlib import Path
import json
from html import unescape

RESIDENTIAL_AREA = 'residential_areas.js'
redidential_area_jsonfile = Path(__file__).parents[2] / RESIDENTIAL_AREA
longitude = 38.7494272
latitude = 8.943757
user_location = Point(longitude, latitude, srid=4326)


class Home(generic.ListView):
    model = School
    context_object_name = 'schools'
    queryset = School.objects.annotate(distance=Distance('location', user_location)).order_by('distance')
    template_name = 'schools/dashboard.html'


class SchoolsDetailView(DetailView):
    template_name = 'schools/detail.html'
    model = School

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['layer_residential_areas'] = unescape(open(redidential_area_jsonfile, 'r').read())

        return context
