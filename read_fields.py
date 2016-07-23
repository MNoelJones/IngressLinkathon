import json
from io import StringIO
from argparse import Namespace

s = StringIO("""
[
    {
        "type": "polyline",
        "latLngs": [
            {
                "lat": 51.260892,
                "lng": -1.081706
            },
            {
                "lat": 51.260552,
                "lng": -1.081721
            },
            {
                "lat": 51.260315,
                "lng": -1.081542
            },
            {
                "lat": 51.260892,
                "lng": -1.081706
            },
            {
                "lat": 51.260892,
                "lng": -1.081706
            }
        ],
        "color": "#a24ac3"
    },
    {
        "type": "polyline",
        "latLngs": [
            {
                "lat": 51.260892,
                "lng": -1.081706
            },
            {
                "lat": 51.260287,
                "lng": -1.08354
            },
            {
                "lat": 51.260315,
                "lng": -1.081542
            }
        ],
        "color": "#a24ac3"
    }
]        """)


def field_factory(json_dict):
    """ Generate an object of the appropriate type from the parsed json. """
    field = Namespace(**json_dict)
    if field.type == "polyline":
        latlngs = field.latLngs
        field.latLngs = [Namespace(**x) for x in latlngs]
        fld = Field()
        fld.__dict__ = field.__dict__
        return fld


class Field(object):
    pass


# with open() as fd:
j = json.loads(s.getvalue())

for field_d in j:
    print("\n")
    field = field_factory(field_d)
    first = None
    for latlng in field.latLngs:
        if first is None:
            first = latlng
        elif not(first.lat == latlng.lat and first.lng == latlng.lng):
            print(
                "LINK ({}, {}) TO ({}, {})".format(
                    first.lat, first.lng,
                    latlng.lat, latlng.lng
                )
            )
            first = latlng
