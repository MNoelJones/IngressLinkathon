import functools


def area_of_triangle(point1, point2, point3):
    (x1, y1, x2, y2, x3, y3) = (point1 + point2 + point3)
    return abs((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))


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
    def __init__(self, portal1=None, portal2=None, **kwargs):
        super(LinkCommand, self).__init__(**kwargs)
        self._portal1 = portal1
        self._portal2 = portal2

    def __call__(self):
        # print "Creating Link from {} to {}".format(
            # self._portal1.name,
            # self._portal2.name
        # )
        if self.player.location == self._portal1.location:
            self._world.create_link(self._portal1, self._portal2)
        else:
            print "Link failed - player not within range of {} ({})".format(
                self._portal1.name,
                self._portal1.location
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

    def create_link(self, portal_from, portal_to):
        world.create_link(portal_from, portal_to)

    def is_at(self, portal):
        return self.location == portal.location


class Portal(object):
    def __init__(self, name=None, guid=None, location=None):
        self.name = name
        self.guid = guid
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
    def __init__(self, portal_from=None, portal_to=None):
        self._from = portal_from
        self._to = portal_to


class Field(object):
    def __init__(self, portals=[]):
        self._portals = portals

    @property
    def portals(self):
        return self._portals


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

    def add_portal(self, name=None, guid=None, location=None):
        portal = Portal(
            name=name,
            guid=guid,
            location=location
        )
        self._portals.append(portal)
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

    def create_field(self, portal1, portal2, portal3):
        self.fields.append(Field([portal1, portal2, portal3]))

    def create_link(self, portal_one, portal_two):
        assert portal_one in self._portals, (
            "Unknown portal, {}".format(portal_one)
        )
        assert portal_two in self._portals, (
            "Unknown portal, {}".format(portal_two)
        )
        print "\nLinking {} to {}".format(portal_one.name, portal_two.name)
        portal_one.add_link(portal_two)
        print "outbound_links for {}: {}".format(
            portal_one.name,
            ",".join(p.name for p in portal_one.outbound_links)
        )
        print "outbound_links for {}: {}".format(
            portal_two.name,
            ",".join(p.name for p in portal_two.outbound_links)
        )
        # Are there any common linked portals for portal_one and portal_two
        potential_field_portals = (
            (set(portal_one.outbound_links) | set(portal_one.inbound_links)) &
            (set(portal_two.outbound_links) | set(portal_two.inbound_links))
        )
        print "potential fields created with: {}\n\n".format(
            potential_field_portals
        )
        if potential_field_portals:
            size_key = functools.partial(
                self.area_of_field,
                portal_one,
                portal_two
            )
            max_field_portal = max(potential_field_portals, key=size_key)
            print "max size field created to: {}".format(max_field_portal.name)
            self.create_field(portal_one, portal_two, max_field_portal)

    def add_player(self, player):
        self.players.append(player)
        player.world = self
