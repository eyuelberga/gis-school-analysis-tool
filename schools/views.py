from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import DetailView
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import get_object_or_404, render

from .forms import DistanceAnalysisForm
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
