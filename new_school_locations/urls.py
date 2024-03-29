"""new_school_locations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from schools import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('school', views.Schools.as_view(), name='schools'),
    path('school/distance_analysis/<lat>/<lng>', views.DistanceAnalysis.as_view(), name='distance_analysis'),
    path('school/distance_analysis', views.DistanceAnalysisFormView.as_view(), name='distance_analysis_form'),
    path('school/suitable_site', views.SuitableSiteFormView.as_view(), name='suitable_site_form'),
    url(r'^school/suitable_site/(?P<pk>[0-9]+)$', views.SuitableSiteView.as_view(), name='suitable_site'),
    url(r'^school/(?P<pk>[0-9]+)$', views.SchoolsDetailView.as_view(), name='detail')
]
