# test_worldsim_parser.py
from unittest import TestCase  # , skip
from worldsim_parser import WorldsimParser
from worldsim_populator import WorldsimPopulator
from worldsim import LinkCommand, World, Player, FieldCommand


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
        player = Player()
        world = World()
        world.add_player(player)
        self.wspopulator = WorldsimPopulator(world=world)

    def test_add_portal_to_world(self):
        """ After adding a portal to the world, it should be accessible """
        instring = """
            ID "Southern Entrance To War Memorial" AS 1
            LOCATE 1 AT 51.258472N,  1.076191W
            GUID 1 47db8ce5d774463f9a8e7aef948e8093.16
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

    def test_ns_ew_locations(self):
        """ A location should allow specification using N, S, E, W. """
        instring = """
            ID "Southern Entrance To War Memorial" AS 1
            LOCATE 1 AT 51.258472N,  -1.076191E
        """
        self.wspopulator.parse(instring)
        portal = self.wspopulator.world.portal[0]
        self.assertEqual(
            portal.name,
            "Southern Entrance To War Memorial"
        )
        self.assertEqual(
            portal.location,
            (51.258472, -1.076191)
        )
        self.wspopulator.parse("LOCATE 1 AT 51.258472N,  1.076191W")
        self.assertEqual(
            portal.location,
            (51.258472, -1.076191)
        )

    def test_fielding_instructions(self):
        """ Fielding instructions should create the links and fields specified. """
        instring = """
            ID "Wote Street Monument" as 1
            ID "Entrance to Black Dam and Crabtree" as 2
            ID "Author Atwood" as 3
            ID "Entrance to War Memorial Park (flat)" as 4
            ID "St.Mary's" as 5
            ID "Canal Heritage Footpath" as 6
            ID "Fossil Post" as 7
            ID "The Boat House" as 8
            ID "Eastrop Park (large)" as 9

            FIELD 1 2 4 as 301
            FIELD 1 2 5 as 302
            FIELD 1 2 6 as 303
            FIELD 2 3 6 as 304
            FIELD 2 6 7 as 305
            FIELD 2 6 8 as 306
            FIELD 2 6 9 as 307
        """
        self.wspopulator.parse(instring)
        commands = self.wspopulator.world.player[0].commands
        fieldcommands = [command for command in commands if isinstance(command, FieldCommand)]
        self.assertItemsEqual(
            [f.field_id for f in fieldcommands],
            ["301", "302", "303", "304", "305", "306", "307"]
        )

    def test_forward_link_instructions(self):
        """ Forward link instructions should create the link specified. """
        instring = """
            ID "Entrance to War Memorial Park (flat)" as 4
            ID "St.Mary's" as 5
            ID "Canal Heritage Footpath" as 6
            LINK 5 4 as 107 FORWARD
            LINK 6 5 as 108 FORWARD
        """
        self.wspopulator.parse(instring)
        commands = self.wspopulator.world.player[0].commands
        linkcommands = [command for command in commands if isinstance(command, LinkCommand)]
        self.assertItemsEqual(
            [l.link_id for l in linkcommands],
            ["107", "108"]
        )
