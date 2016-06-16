# test_worldsim_parser.py
from unittest import TestCase
from worldsim_parser import WorldsimParser


class TestWorldsimParser(TestCase):
    def setUp(self):
        self.parser = WorldsimParser()

    def test_ID(self):
        instring = 'ID "Southern Entrance To War Memorial" AS 1'
        assert self.parser.parseString(instring)

    def test_Field(self):
        self.fail()

    def test_Link(self):
        self.fail()

    def test_Locate(self):
        self.fail()

    def test_Guid(self):
        self.fail()

    def test_Move(self):
        self.fail()