class Player(object):
    def __init__(self, world=None, commands=None):
        self._world = world
        self._command_list = commands
        self.location = None

    @property
    def commands(self):
        return self._command_list

    def add_command(self, command):
        self.command.append(command)

    def create_link(self, portal_from, portal_to):
        world.create_link(portal_from, portal_to)

    def is_at(self, portal):
        return self.location == portal.location


class Portal(object):
    def __init__(self, name=None, guid=None, location=None):
        self.name = name
        self.guid = guid
        self.location = location
        self.linked_portals = []

    def is_linked_to(self, portal):
        return portal in self.linked_portals

    def add_link(self, portal):
        if portal not in self.linked_portals:
            self.linked_portals.append(portal)


class Link(object):
    def __init__(self, portal_from=None, portal_to=None):
        self._from = portal_from
        self._to = portal_to


class Field(object):
    def __init__(self, portals=[]):
        self._portals = portals


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

    def add_portal(self, name=None, guid=None, location=None):
        portal = Portal(
            name=name,
            guid=guid,
            location=location
        )
        self._portals.append(portal)
        return portal

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

    def create_link(self, portal_one, portal_two):
        assert portal_one in self._portals, (
            "Unknown portal, {}".format(portal_one)
        )
        assert portal_two in self._portals, (
            "Unknown portal, {}".format(portal_two)
        )
        portal_one.add_link(portal_two)

    def add_player(self, player):
        self.players.append(player)
        player.world = self
