# worldsim_populator.py
from worldsim import World, LinkCommand, FieldCommand
from worldsim_parser import WorldsimParser


class AWorldsimParser(WorldsimParser):
    def __init__(self, world):
        super(AWorldsimParser, self).__init__()
        self._world = world

    @property
    def world(self):
        return self._world

    def id_command_action(self, toks):
        print "Aworldsim_parser: {}".format(toks)
        self.world.add_portal(name=toks[0], id=toks[1])

    def guid_command_action(self, toks):
        print "Aworldsim_parser: {}".format(toks)
        try:
            portal = self.world.find_portal(toks[0])
            portal.guid = toks[1]
        except AttributeError:
            print "No portal with ID {}".format(toks[0])

    def locate_command_action(self, toks):
        print "Aworldsim_parser: {}".format(toks)
        (id, lat, ns, lng, ew) = toks
        if ns == "S":
            lat = -lat
        if ew == "W":
            lng = -lng
        portal = self.world.find_portal(id)
        portal.location = (lat, lng)

    def field_request_action(self, toks):
        print "Aworldsim_parser: {}".format(toks)
        (p1, p2, p3, fid) = toks
        cmd = FieldCommand(portals=[p1, p2, p3], field_id=fid, world=self.world)
        self.world.player[0].commands.append(cmd)
        # self.world.create_field(p1, p2, p3, field_id=fid)

    def link_request_action(self, toks):
        print "Aworldsim_parser (LINK): {}".format(toks)
        (p1, p2, lid, fwd) = toks
        cmd = LinkCommand(portal1=p1, portal2=p2, link_id=lid, world=self.world)
        self.world.player[0].commands.append(cmd)


class WorldsimPopulator(object):
    def __init__(self, world=None):
        self._world = world or World()
        self.parser = AWorldsimParser(self.world)

    @property
    def world(self):
        return self._world

    def parse(self, instring):
        self.parser.parseString(instring)
