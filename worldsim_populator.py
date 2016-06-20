# worldsim_populator.py
from worldsim import World
from worldsim_parser import WorldsimParser


class WorldsimPopulator(object):
    def __init__(self, world=None):
        self._world = world or World()
        self.parser = WorldsimParser()

    @property
    def world(self):
        return self._world

    def parse(self, instring):
        self.parser.parseString(instring)
