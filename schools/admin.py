from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin
from .models import School


@admin.register(School)
class SchoolAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')
