# test_worldsim_parser.py
from unittest import TestCase  # , skip
from worldsim_parser import WorldsimParser
from worldsim_populator import WorldsimPopulator


class TestWorldsimParser(TestCase):
    def setUp(self):
        self.parser = WorldsimParser()

    def test_ID(self):
        instring = 'ID "Southern Entrance To War Memorial" AS 1'
        assert self.parser.parseString(instring)

    def test_Field(self):
        instring = 'FIELD 1 2 3    AS 20'
        assert self.parser.parseString(instring)

    def test_Link(self):
        # instring = "LINK 2 12      AS 101 # Kicker for 20-28"
        instring = "LINK 2 12      AS 101"
        assert self.parser.parseString(instring)

    def test_Locate(self):
        instring = "LOCATE 1 AT 51.258472N,  -1.076191E"
        assert self.parser.parseString(instring)

    def test_Guid(self):
        instring = "GUID 1 47db8ce5d774463f9a8e7aef948e8093.16"
        assert self.parser.parseString(instring)

    def test_Move(self):
        instring = "MOVE 51.258472N, -1.076191E"
        assert self.parser.parseString(instring)

    def test_Comment(self):
        instring = "MOVE 51.258472N, -1.076191E # Over the rainbow"
        assert self.parser.parseString(instring)


class TestWorldsimPopulator(TestCase):
    def setUp(self):
        self.wspopulator = WorldsimPopulator()

    def test_add_portal_to_world(self):
        """ After adding a portal to the world, it should be accessible """
        instring = """
            ID "Southern Entrance To War Memorial" AS 1
        """
        # """
        # LOCATE 1 AT 51.258472N,  -1.076191E
        # GUID 1 47db8ce5d774463f9a8e7aef948e8093.16
        # """
        self.wspopulator.parse(instring)
        portal = self.wspopulator.world.portal[0]
        self.assertEqual(
            portal.name,
            "Southern Entrance To War Memorial"
        )
        self.assertEqual(
            portal.guid,
            "47db8ce5d774463f9a8e7aef948e8093.16"
        )
        self.assertEqual(
            portal.location,
            (51.258472, -1.076191)
        )
