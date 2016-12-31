
def area_of_triangle(point1, point2, point3):
    (x1, y1, x2, y2, x3, y3) = (point1 + point2 + point3)
    return abs((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))


def bary(point1, point2, point3, point4):
    (x1, y1) = point1
    (x2, y2) = point2
    (x3, y3) = point3
    (x, y) = point4
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
    except BaseException:
        raise ValueError
    c = 1 - a - b
    return (a, b, c)


def point_in_triangle(p, p1, p2, p3):
    try:
        (a, b, c) = bary(p1, p2, p3, p)
    except BaseException as err:
        print("Exception ({}) {} {} {} {}".format(err, p1, p2, p3, p))
        return False
    return (0 <= a <= 1 and
            0 <= b <= 1 and
            0 <= c <= 1)


class Command(object):
    def __init__(self, world=None, player=None):
        self._world = world
        self._player = player

    def __call__(self):
        pass

    @property
    def world(self):
        return self._world

    @property
    def player(self):
        return self._player

    @world.setter
    def world(self, val):
        self._world = val

    @player.setter
    def player(self, val):
        self._player = val


class LinkCommand(Command):
    def __init__(self, portal1=None, portal2=None, link_id=None, **kwargs):
        super(LinkCommand, self).__init__(**kwargs)
        self._portal1 = portal1
        self._portal2 = portal2
        self._link_id = link_id

    def __str__(self):
        return "LINK {} {}{}".format(
            self._portal1.id,
            self._portal2.id,
            "" if self._link_id is None else "AS {}".format(self._link_id)
        )

    def __call__(self):
        # print "Creating Link from {} to {}".format(
            # self._portal1.name,
            # self._portal2.name
        # )
        if self.player.location == self._portal1.location:
            self._world.create_link(self._portal1, self._portal2)
        else:
            print(
                "Link failed - player not within range of {} ({})".format(
                    self._portal1.name,
                    self._portal1.location
                )
            )


class MoveCommand(Command):
    def __init__(self, location=None, **kwargs):
        super(MoveCommand, self).__init__(**kwargs)
        self._location = location

    def __repr__(self):
        return "MoveCommand(location={}, world={}, player={})".format(
            self._location,
            self._world,
            self._player
        )

    def __call__(self):
        # print "Setting player location to {}".format(self._location)
        self.player.location = self._location


class Player(object):
    def __init__(self, world=None, commands=None):
        self._world = world
        self._command_list = commands or []
        self.location = None

    @property
    def commands(self):
        return self._command_list

    @property
    def command(self):
        return self._command_list

    def add_command(self, command):
        self.commands.append(command)
        command.world = self.world
        command.player = self

    def create_link(self, portal_from, portal_to, link_id=None):
        self._world.create_link(portal_from, portal_to, link_id=link_id)

    def is_at(self, portal):
        return self.location == portal.location


class Portal(object):
    def __init__(self, name=None, id=None, location=None):
        self.name = name
        self.id = id  # ID by which the portal is referred to in worldsim
        self.guid = None  # Ingress GUID
        self.location = location
        self.outbound_links = []
        self.inbound_links = []

    def is_linked_to(self, portal):
        return portal in self.outbound_links

    def is_linked_from(self, portal):
        return portal in self.inbound_links

    def add_link(self, portal):
        if (not self.is_linked_to(portal) and not self.is_linked_from(portal)):
            self.outbound_links.append(portal)
            portal.inbound_links.append(self)


class Link(object):
    def __init__(self, portal_from=None, portal_to=None, link_id=None):
        self._from = portal_from
        self._to = portal_to
        self._link_id = link_id

    @property
    def link_id(self):
        return self._link_id


class Field(object):
    def __init__(self, portals=None, field_id=None):
        self._portals = portals
        self._field_id = field_id

    @property
    def portals(self):
        return self._portals

    @property
    def field_id(self):
        return self._field_id

    def portal_inside_field(self, portal):
        (p1, p2, p3) = [p.location for p in self.portals]
        p = portal.location
        return point_in_triangle(p, p1, p2, p3)


class World(object):
    def __init__(self):
        self._players = []
        self._portals = []
        self._links = []
        self._fields = []

    @property
    def portal(self):
        return self._portals

    @property
    def players(self):
        return self._players

    @property
    def player(self):
        return self._players

    @property
    def fields(self):
        return self._fields

    @property
    def links(self):
        return self._links

    def add_portal(self, name=None, id=None, location=None):
        portal = Portal(
            name=name,
            id=id,
            location=location
        )
        self._portals.append(portal)
        return portal

    def find_portal(self, id):
        portal = None
        try:
            portal = [p for p in self.portal if p.id == id][0]
        except IndexError:
            print "No portal with ID {}".format(toks[0])
        return portal

    def field_exists(self, portal1, portal2, portal3):
        expected_portals = set([portal1, portal2, portal3])
        for field in self.fields:
            if set(field.portals) == expected_portals:
                return True
        return False

    def link_exists(self, portal_one, portal_two):
        assert portal_one in self._portals, (
            "Unknown portal, {}".format(portal_one)
        )
        assert portal_two in self._portals, (
            "Unknown portal, {}".format(portal_two)
        )
        return (
            portal_one.is_linked_to(portal_two) or
            portal_two.is_linked_to(portal_one)
        )

    def area_of_field(self, portal1, portal2, portal3):
        return area_of_triangle(
            portal1.location,
            portal2.location,
            portal3.location
        )

    def create_field(self, portal1, portal2, portal3, field_id=None):
        self.fields.append(Field(portals=[portal1, portal2, portal3], field_id=field_id))

    def portal_within_field(self, portal):
        """ Test if a portal is within any existing fields. """
        for field in self.fields:
            if point_in_triangle(
                portal.location,
                *[x.location for x in field.portals]
            ):
                return True
        return False

    def create_link(self, portal_one, portal_two, link_id=None):
        assert portal_one in self._portals, (
            "Unknown portal, {}".format(portal_one)
        )
        assert portal_two in self._portals, (
            "Unknown portal, {}".format(portal_two)
        )
        if self.portal_within_field(portal_one):
            raise ValueError  # ("Portal inside a field")
        print("Linking {} to {}".format(portal_one.name, portal_two.name))
        portal_one.add_link(portal_two)
        # Are there any common linked portals for portal_one and portal_two
        potential_field_portals = (
            (set(portal_one.outbound_links) | set(portal_one.inbound_links)) &
            (set(portal_two.outbound_links) | set(portal_two.inbound_links))
        )
        if potential_field_portals:
            handled1 = []
            pfp = list(potential_field_portals)
            idx1 = 0
            while idx1 < len(pfp):
                item = pfp[idx1]
                idx2 = 0
                while idx2 < len(pfp):
                    test_portal = pfp[idx2]
                    if test_portal is not item:
                        if point_in_triangle(
                            test_portal.location,
                            item.location,
                            portal_one.location,
                            portal_two.location
                        ):
                            pfp.remove(test_portal)
                        else:
                            print("No.\n")
                    idx2 += 1
                idx1 += 1

            for field_portal in pfp:
                print(
                    "\nCreating field: {} -> {} -> {}\n".format(
                        portal_one.name,
                        portal_two.name,
                        field_portal.name
                    )
                )
                self.create_field(portal_one, portal_two, field_portal)

    def add_player(self, player):
        self.players.append(player)
        player.world = self
