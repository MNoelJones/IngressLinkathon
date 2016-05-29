def bary(p1, p2, p3, p):
    (x1, y1) = p1
    (x2, y2) = p2
    (x3, y3) = p3
    (x, y) = p
    try:
        a = (
                (y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)
            ) / (
                (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
            )
        b = (
                (y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)
            ) / (
                (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
            )
    except BaseException as err:
        raise ValueError(err)
    c = 1 - a - b
    return (a, b, c)


def point_in_triangle(p, p1, p2, p3):
    try:
        (a, b, c) = bary(p1, p2, p3, p)
    except:
        print "Exception {} {} {} {}".format(p1, p2, p3, p)
        return False
    return (0 <= a <= 1 and
            0 <= b <= 1 and
            0 <= c <= 1)


class Portal(object):
    def __init__(self):
        self._name = None
        self._location = (None, None)
        self._id = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location

    @id.setter
    def id(self, val):
        self._id = val

    @name.setter
    def name(self, val):
        self._name = val

    @location.setter
    def location(self, val):
        self._location = val


class Field(object):
    def __init__(self, *portals):
        self._portals = portals

    @property
    def portals(self):
        return self._portals

    def portal_inside_field(self, portal):
        (p1, p2, p3) = [p.location for p in self.portals]
        p = portal.location
        return point_in_triangle(p, p1, p2, p3)


class Linkathon(object):
    def __init__(self):
        self.fields = {}
        self.portals = {}
        self.links = {}
        self.ids = {}
        self._field_id = 0
        self._portal_id = 0
        self._link_id = 0
        self._id_id = 0

    @property
    def field(self):
        return self.fields

    @property
    def portal(self):
        return self.portals

    @property
    def link(self):
        return self.links

    @property
    def id(self):
        return self.ids

    @field.setter
    def field(self, value):
        self.fields.update(value)

    @portal.setter
    def portal(self, value):
        self.portals.update(value)

    @link.setter
    def link(self, value):
        self.links.update(value)

    @id.setter
    def id(self, value):
        self.ids.update(value)
