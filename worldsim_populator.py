# worldsim_populator.py
from worldsim import World
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
        self.world.add_portal(name=toks[0], guid=toks[1])


class WorldsimPopulator(object):
    def __init__(self, world=None):
        self._world = world or World()
        self.parser = AWorldsimParser(self.world)

    @property
    def world(self):
        return self._world

    def parse(self, instring):
        self.parser.parseString(instring)
