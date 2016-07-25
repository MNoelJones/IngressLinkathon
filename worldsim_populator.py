# worldsim_populator.py
from worldsim import World
from worldsim_parser import WorldsimParser


class AWorldsimParser(WorldsimParser):
    def __init__(self):
        super(AWorldsimParser, self).__init__()

    def id_command_action(selfi, toks):
        print "Aworldsim_parser: {}".format(toks)


class WorldsimPopulator(object):
    def __init__(self, world=None):
        self._world = world or World()
        self.parser = AWorldsimParser()

    @property
    def world(self):
        return self._world

    def parse(self, instring):
        self.parser.parseString(instring)
