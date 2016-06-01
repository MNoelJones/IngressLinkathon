# test_worldsim.py
from unittest import TestCase
from worldsim import World, Player, LinkCommand, MoveCommand


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

    def create_portals(self):
        portals = {}
        locations = [
            (51.258472, -1.076191),
            (51.258623, -1.081081),
            (51.260184, -1.088666),
            (51.260287, -1.083540),
            (51.259231, -1.084654),
            (51.258658, -1.081617),
            (51.261578, -1.083193),
            (51.262180, -1.082827),
            (51.261766, -1.082850),
            (51.261324, -1.083513),
            (51.261720, -1.082287),
            (51.259443, -1.083362),
            (51.260750, -1.083664),
            (51.260892, -1.081706),
            (51.259620, -1.081563),
            (51.260552, -1.081721),
            (51.260315, -1.081542),
        ]

        names = [
            ("Southern Entrance To War Memorial"),
            ("If Aught of Oaten"),
            ("The Bounty Inn Pub"),
            ("I Saw The Hare"),
            ("Diana Stanley Memorial Plaque"),
            ("War Memorial Playground"),
            ("Torch"),
            ("Civic Centre War Memorial"),
            ("War Memorial Park"),
            ("Memorial Park Aviary"),
            ("Shelter Dedication Plaque"),
            ("The Golden Tree Engraving"),
            ("Memorial Band Stand"),
            ("Kath And Gordon Ball Memorial"),
            ("Winnie White Memorial Bench"),
            ("Tree Planting Ceremony Plaque"),
            ("Ivy & George White Plaque"),
        ]
        guids = [
            "47db8ce5d774463f9a8e7aef948e8093.16",
            "7d2c6ea6b74d40d18147ee73dbcd802f.16",
            "19bee196d8964d378807c8e7effce827.16",
            "2d9e4c7fe8dc48679e3a0f59b04287aa.16",
            "4f00ca7279b14c16b1107939be671ea7.16",
            "2ad0c389e094410384f10f74fd2e1250.16",
            "b629547a87d7432d90f8e27577e7dc99.16",
            "9c7e56e4e505450faeb0f81389cc80bf.11",
            "4b1b025b6fbe460e980d4db347993ca9.16",
            "c7c1ca91df9145b0bc3b894033d1ea4f.11",
            "41de7df2cc3a4e91b5a2f9c24e92e4e2.16",
            "bd059ba73a7c4307a8b04920ff7806dc.16",
            "032428ea97494692a221337cf19287b2.16",
            "dc9b9457816c47f69766f3e2c29e8c4b.16",
            "f3a3d5806b2446caa3df67432700a49e.16",
            "2286f18bad3e47fea698d38cd5f01f39.16",
            "fb88168cc2774b1cac1da52daa7bd40a.16",
        ]
        portals = [
            self.world.add_portal(
                name=x[0],
                location=x[1],
                guid=x[2]
            )
            for x in zip(names, locations, guids)
        ]
        return portals

    create_two_portals = create_portals
    create_three_portals = create_portals
    create_four_portals = create_portals

    def test_link_portals(self):
        """
            Verify Link Creation.

            After creating a link, it should be possible to
            verify from either portal
        """
        portals = self.create_two_portals()
        self.world.create_link(portals[0], portals[1])
        self.assertTrue(self.world.link_exists(portals[0], portals[1]))
        self.assertTrue(self.world.link_exists(portals[1], portals[0]))

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

    def add_player_to_world(self):
        player = Player()
        self.world.add_player(player)
        return player

    def test_player_command_link(self):
        """
            A player may have a command to link two portals.
            The existence of the command on the player should not cause
            the portals to be linked in the world until it is executed.
        """
        player = self.add_player_to_world()
        portals = self.create_two_portals()
        player.location = portals[0].location
        command = LinkCommand(portal1=portals[0], portal2=portals[1])
        player.add_command(command)
        self.assertFalse(self.world.link_exists(portals[0], portals[1]))
        player.command[0]()
        self.assertTrue(self.world.link_exists(portals[0], portals[1]))

    def test_player_cannot_link_from_afar(self):
        """
            A player cannot execute a command to link a portal
            if they are not located within 40m of that portal
        """
        player = self.add_player_to_world()
        portals = [
            p for y in [
                "Southern Entrance To War Memorial",
                "The Bounty Inn Pub",
                "Winnie White Memorial Bench",
                "I Saw The Hare"
            ] for p in self.create_four_portals() if p.name == y
        ]
        player.add_command(MoveCommand(portals[3].location))
        player.command[0]()
        command = LinkCommand(portal1=portals[0], portal2=portals[1])
        player.add_command(command)
        self.assertFalse(self.world.link_exists(portals[0], portals[1]))
        player.command[1]()
        self.assertFalse(self.world.link_exists(portals[0], portals[1]))

    def test_player_links_three_portals_into_field(self):
        """
            A player connects three portals with links.
            As well as the links created, a field is formed in the `world`.
        """
        player = self.add_player_to_world()
        portals = [
            p for y in [
                "Southern Entrance To War Memorial",
                "The Bounty Inn Pub",
                "Winnie White Memorial Bench",
            ] for p in self.create_four_portals() if p.name == y
        ]
        player.add_command(MoveCommand(portals[0].location))
        player.add_command(LinkCommand(
            portal1=portals[0],
            portal2=portals[1]
        ))
        player.add_command(LinkCommand(
            portal1=portals[0],
            portal2=portals[2]
        ))
        player.add_command(MoveCommand(portals[1].location))
        player.add_command(LinkCommand(
            portal1=portals[1],
            portal2=portals[2]
        ))
        self.assertFalse(self.world.link_exists(portals[0], portals[1]))
        self.assertFalse(self.world.link_exists(portals[0], portals[2]))
        self.assertFalse(self.world.link_exists(portals[1], portals[2]))
        self.assertFalse(self.world.field_exists(
            portals[0],
            portals[1],
            portals[2]
        ))
        for command in player.commands:
            command()
        self.assertTrue(self.world.link_exists(portals[0], portals[1]))
        self.assertTrue(self.world.link_exists(portals[0], portals[2]))
        self.assertTrue(self.world.link_exists(portals[1], portals[2]))
        self.assertTrue(self.world.field_exists(
            portals[0],
            portals[1],
            portals[2]
        ))

    def test_larger_field_is_chosen(self):
        """
            A player connects three portals with links.
            As well as the links created, a field is formed in the `world`.
        """
        player = self.add_player_to_world()
        portals = [
            p for y in [
                "Southern Entrance To War Memorial",
                "The Bounty Inn Pub",
                "Winnie White Memorial Bench",
                "Ivy & George White Plaque"
            ] for p in self.create_four_portals() if p.name == y
        ]
        player.add_command(MoveCommand(portals[2].location))
        player.add_command(LinkCommand(
            portal1=portals[2],
            portal2=portals[0]
        ))
        player.add_command(LinkCommand(
            portal1=portals[2],
            portal2=portals[1]
        ))
        player.add_command(MoveCommand(portals[3].location))
        player.add_command(LinkCommand(
            portal1=portals[3],
            portal2=portals[0]
        ))
        player.add_command(LinkCommand(
            portal1=portals[3],
            portal2=portals[1]
        ))
        player.add_command(MoveCommand(portals[0].location))
        player.add_command(LinkCommand(
            portal1=portals[0],
            portal2=portals[1]
        ))
        self.assertFalse(self.world.link_exists(portals[2], portals[0]))
        self.assertFalse(self.world.link_exists(portals[2], portals[1]))
        self.assertFalse(self.world.link_exists(portals[3], portals[0]))
        self.assertFalse(self.world.link_exists(portals[3], portals[1]))
        self.assertFalse(self.world.link_exists(portals[0], portals[1]))
        self.assertFalse(self.world.field_exists(
            portals[0],
            portals[1],
            portals[2]
        ))
        self.assertFalse(self.world.field_exists(
            portals[0],
            portals[1],
            portals[3]
        ))
        for command in player.commands:
            command()
        self.assertTrue(self.world.link_exists(portals[0], portals[1]))
        self.assertTrue(self.world.link_exists(portals[0], portals[2]))
        self.assertTrue(self.world.link_exists(portals[1], portals[2]))
        self.assertFalse(self.world.field_exists(
            portals[0],
            portals[1],
            portals[2]
        ))
        self.assertTrue(self.world.field_exists(
            portals[0],
            portals[1],
            portals[3]
        ))

    def test_cannot_link_from_portal_inside_field(self):
        pass
