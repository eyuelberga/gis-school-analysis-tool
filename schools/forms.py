from django.contrib.gis import forms


class DistanceAnalysisForm(forms.Form):
    location = forms.PointField(widget=forms.OSMWidget(
        attrs={'map_width': 700, 'map_height': 500, 'default_lat': 8.9806, 'default_lon': 38.7578}))

