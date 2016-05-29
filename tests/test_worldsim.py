# test_worldsim.py
from unittest import TestCase
from worldsim import World, Player


class TestWorldsim(TestCase):
    def setUp(self):
        self.world = World()

    def test_add_portal_to_world(self):
        """ After adding a portal to the world, it should be accessible """
        # LOCATE 1 AT 51.258472,  -1.076191
        # GUID 1 47db8ce5d774463f9a8e7aef948e8093.16
        portal = self.world.add_portal(
            name="Southern Entrance To War Memorial",
            guid="47db8ce5d774463f9a8e7aef948e8093.16",
            location=(51.258472,  -1.076191)
        )
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

    def test_link_portals(self):
        """
            Verify Link Creation.

            After creating a link, it should be possible to
            verify from either portal
        """
        portals = {}
        portals["1"] = self.world.add_portal(
            name="Southern Entrance To War Memorial",
            guid="47db8ce5d774463f9a8e7aef948e8093.16",
            location=(51.258472,  -1.076191)
        )
        # ID "If Aught of Oaten" AS 2
        # LOCATE 2 AT 51.258623,  -1.081081
        # GUID 2 7d2c6ea6b74d40d18147ee73dbcd802f.16
        portals["2"] = self.world.add_portal(
            name="If Aught of Oaten",
            guid="7d2c6ea6b74d40d18147ee73dbcd802f.16",
            location=(51.258623,  -1.081081)
        )
        self.world.create_link(portals["1"], portals["2"])
        self.assertTrue(self.world.link_exists(portals["1"], portals["2"]))
        self.assertTrue(self.world.link_exists(portals["2"], portals["1"]))

    def test_add_player_to_the_world(self):
        """
            When a player is added to the world,
            the player should have a reference to the world
            and the world should have a reference to the player
        """
        player = Player()
        self.world.add_player(player)
        self.assertEqual(player.world, self.world)
        self.assertEqual(player, self.world.players[0])
