from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin
from .models import School, ResidentialArea


@admin.register(School)
class SchoolAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')


@admin.register(ResidentialArea)
class ResidentialAreaAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')
