# test_linkathon.py
from unittest import TestCase
import linkathon


class TestLinkathon(TestCase):
    def setUp(self):
        names_to_ids = {
            "Diana Stanley Memorial Plaque": 5,
            "War Memorial Playground": 6,
            "Torch": 7,
            "Civic Centre War Memorial": 8,
            "War Memorial Park": 9,
            "Memorial Park Aviary": 10,
            "Shelter Dedication Plaque": 11,
            "The Golden Tree Engraving": 12,
            "Memorial Band Stand": 13,
            "Kath And Gordon Ball Memorial": 14,
            "Winnie White Memorial Bench": 15,
            "Tree Planting Ceremony Plaque": 16,
            "Ivy & George White Plaque": 17,
            "Southern Entrance To War Memorial": 1,
            "If Aught of Oaten": 2,
            "The Bounty Inn Pub": 3,
            "I Saw The Hare": 4,
        }

        fields = {
            'field_20': [1, 2, 3],
            'field_21': [1, 3, 6],
            'field_22': [1, 3, 15],
            'field_23': [1, 3, 17],
            'field_24': [1, 3, 16],
            'field_25': [1, 3, 14],
            'field_26': [1, 3, 11],
            'field_27': [1, 3, 8],
            'field_28': [1, 3, 12],
            'field_50': [3, 6, 5],
            'field_51': [3, 6, 2],
            'field_52': [3, 4, 17],
            'field_53': [3, 13, 14],
            'field_54': [3, 10, 14],
            'field_55': [3, 9, 11],
            'field_56': [3, 7, 11],
        }
        locations = {
            'node_1': (51.258472, -1.076191),
            'node_2': (51.258623, -1.081081),
            'node_3': (51.260184, -1.088666),
            'node_4': (51.260287, -1.083540),
            'node_5': (51.259231, -1.084654),
            'node_6': (51.258658, -1.081617),
            'node_7': (51.261578, -1.083193),
            'node_8': (51.262180, -1.082827),
            'node_9': (51.261766, -1.082850),
            'node_10': (51.261324, -1.083513),
            'node_11': (51.261720, -1.082287),
            'node_12': (51.259443, -1.083362),
            'node_13': (51.260750, -1.083664),
            'node_14': (51.260892, -1.081706),
            'node_15': (51.259620, -1.081563),
            'node_16': (51.260552, -1.081721),
            'node_17': (51.260315, -1.081542),
        }

        ids_to_names = [
            (1, "Southern Entrance To War Memorial"),
            (2, "If Aught of Oaten"),
            (3, "The Bounty Inn Pub"),
            (4, "I Saw The Hare"),
            (5, "Diana Stanley Memorial Plaque"),
            (6, "War Memorial Playground"),
            (7, "Torch"),
            (8, "Civic Centre War Memorial"),
            (9, "War Memorial Park"),
            (10, "Memorial Park Aviary"),
            (11, "Shelter Dedication Plaque"),
            (12, "The Golden Tree Engraving"),
            (13, "Memorial Band Stand"),
            (14, "Kath And Gordon Ball Memorial"),
            (15, "Winnie White Memorial Bench"),
            (16, "Tree Planting Ceremony Plaque"),
            (17, "Ivy & George White Plaque"),
        ]

        l = self.l = linkathon.Linkathon()
        for id, name in ids_to_names:
            p = linkathon.Portal()
            p.name = name
            p.id = id
            l.portals.update({p.name: p})
        for (ix, p) in ((l.portals[name].id, l.portals[name])
                        for name in l.portals):
            loc = locations["node_{}".format(ix)]
            p.location = loc
        l.fields.update({
            y: linkathon.Field(portals=[
                p for x in fields[y]
                for p in l.portals.values()
                if p.id == x
            ])
            for y in fields
        })

    def test_port_in_field(self):
        field = self.l.field['field_23']
        portal = self.l.portal['Winnie White Memorial Bench']
        self.assertTrue(field.portal_inside_field(portal))
        portal = self.l.portal["Tree Planting Ceremony Plaque"]
        self.assertFalse(field.portal_inside_field(portal))
