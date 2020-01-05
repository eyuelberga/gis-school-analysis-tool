import math

from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import DetailView
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance, Area, Centroid
from django.shortcuts import get_object_or_404, render

from .forms import DistanceAnalysisForm
from .models import School, ResidentialArea

longitude = 38.7494272
latitude = 8.943757


class Home(generic.ListView):
    template_name = 'schools/dashboard.html'

    def get_queryset(self):
        queryset = School.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schools'] = School.objects.all().count()
        context['residential_areas'] = ResidentialArea.objects.all().count()

        return context


class Schools(generic.ListView):
    model = School
    context_object_name = 'schools'
    queryset = School.objects.all()
    template_name = 'schools/schools.html'


class DistanceAnalysisFormView(generic.View):
    form_class = DistanceAnalysisForm
    template_name = 'schools/distance_analysis_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            target_coord = SpatialReference(4326)
            form_coord = SpatialReference(3857)
            pnt = data['location']
            pnt.transform(CoordTransform(form_coord, target_coord))
            return HttpResponseRedirect('/school/distance_analysis/' + str(pnt.x) + '/' + str(pnt.y))
        return render(request, self.template_name, {'form': form})


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


class SuitableSiteView(DetailView):
    template_name = 'schools/suitable_site.html'
    model = ResidentialArea
    context_object_name = 'residential_area'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = ResidentialArea.objects.annotate(area=Area("location"), centroid=Centroid("location")).get(
            pk=self.kwargs['pk'])
        schools_nearby = School.objects.annotate(distance=Distance('location', obj.centroid)).order_by('distance')[0:6]
        context['area'] = obj.area
        # population density in addis ababa is 5165/km2
        population = 5165 * obj.area.sq_km
        # 43 % of the population is a student
        students = population * (43 / 100)
        # one school holds more than 10,000 students
        no_schools = math.ceil(students / 10000)
        context['closest_school'] = schools_nearby[0]
        context['proximity_criteria'] = schools_nearby[0].distance.km <= 5.0
        context['size_criteria'] = schools_nearby[0].distance.km <= 5.0 if no_schools == 1 else schools_nearby[
                                                                                                    0].distance.km <= 5.0 and \
                                                                                                schools_nearby[
                                                                                                    1].distance.km <= 5.0
        context['overall'] = context['size_criteria'] and context['proximity_criteria']
        return context


class SuitableSiteFormView(generic.ListView):
    template_name = 'schools/suitable_site_form.html'
    model = ResidentialArea
    context_object_name = 'residential_areas'

    def get_queryset(self):
        queryset = ResidentialArea.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            target_coord = SpatialReference(4326)
            form_coord = SpatialReference(3857)
            pnt = data['location']
            pnt.transform(CoordTransform(form_coord, target_coord))
            return HttpResponseRedirect('/school/distance_analysis/' + str(pnt.x) + '/' + str(pnt.y))
        return render(request, self.template_name, {'form': form})
