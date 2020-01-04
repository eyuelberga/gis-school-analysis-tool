from pathlib import Path

import json

from django.contrib.gis.geos import Polygon, MultiPolygon

DATA_FILENAME = 'residential_area_data1.json'


def load_data():
    # ResidentialArea = apps.get_model('schools', 'ResidentialArea')
    jsonfile = "./" + DATA_FILENAME

    with open(str(jsonfile)) as datafile:
        objects = json.load(datafile)
        for obj in objects['features']:
            try:
                objType = obj['geometry']['type']
                properties = obj['properties']
                objGeometry = obj['geometry']
                name = properties.get('mvt_id', 'no-name')
                coordinates = objGeometry.get('coordinates', [])
                if objType == 'Polygon':

                    location = MultiPolygon(Polygon(coordinates[0]), srid=4326)
                    ResidentialArea(name=name, location=location).save()
                elif objType == 'MultiPolygon':
                    location = MultiPolygon(Polygon(coordinates[0][0]), srid=4326)
                    ResidentialArea(name=name, location=location).save()
            except KeyError:
                pass


load_data()
