"""Inventory BDD Tests."""
from unittest import TestCase
from nose2.tools import params
import Inventory


class TestAddItem(TestCase):
    """It should allow you to add any Item to it."""

    def setUp(self):
        self.inventory = Inventory.Inventory()

    def test_newinventory_is_empty(self):
        """A newly created Inventory should be an_empty_inventory."""
        self.assertEqual(self.inventory.invcount(), 0)

    def test_addamod(self):
        """After adding a mod the_size_should_be_one."""
        item = Inventory.Mod()
        self.inventory.add(item)
        self.assertEqual(self.inventory.invcount(), 1)


class TestPopulatedInventory(TestCase):
    def setUp(self):
        self.inventory = Inventory.Inventory()
        counts = {
            "Resonator": 10,
            "Mod": 5
        }
        for item, num in counts.iteritems():
            for _ in range(0, num):
                self.inventory.add(getattr(Inventory, item)())

    def test_item_count(self):
        """ With the above initialisation, invenetory count must be 15."""
        self.assertEqual(self.inventory.itemcount(), 15)

    def test_resonator_count(self):
        """ ...and the resonator count should be 10."""
        count = reduce(
            lambda a, b: a + b.invcount(),
            self.inventory.resonators,
            0
        )
        self.assertEqual(count, 10)

    def test_mod_count(self):
        """ ...and the mod count should be 5."""
        count = reduce(lambda a, b: a + b.invcount(), self.inventory.mods, 0)
        self.assertEqual(count, 5)

    def test_immediate_count(self):
        self.assertEqual(self.inventory.invcount(), 15)

    def test_capsule_addition(self):
        """
        Adding a capsule with 5 items.

        Should make both item and inventory counts equal 6.
        """
        capsule = Inventory.Capsule()
        for _ in range(0, 5):
            capsule.add(Inventory.Resonator())
        self.inventory.add(capsule)

        self.assertEqual(self.inventory.itemcount(), 20)
        self.assertEqual(self.inventory.invcount(), 21)

    def test_keylocker_addition(self):
        """
        When adding_a_keylocker_with_5_keys,
        item and inventory counts should differ.
        """
        locker = Inventory.KeyCapsule()
        for _ in range(0, 5):
            locker.add(Inventory.Key())
        self.inventory.add(locker)

        self.assertEqual(self.inventory.itemcount(), 20)
        self.assertEqual(self.inventory.invcount(), 16)


class TestProcessTransaction(TestCase):
    def setUp(self):
        self.inventory = Inventory.Inventory()

    from collections import namedtuple
    ItemLevelCount = namedtuple("ItemLevelCount", ["count", "level"])

    @params(
        (
            "individual item",
            "CR INV 5 X8",
            {
                "bursters": ItemLevelCount(level=8, count=5)
            }
        ),
        (
            "multiple items",
            "CR INV 5 X8 3 R6",
            {
                "bursters": ItemLevelCount(level=8, count=5),
                "resonators": ItemLevelCount(level=6, count=3)
            }
        )
    )
    def test_credit_transaction(self, name, transaction, conditions):
        self.inventory.apply_transaction(transaction)
        for prop, condition in conditions.iteritems():
            self.assertEqual(len(getattr(self.inventory, prop)), condition.count)
            self.assertTrue(all(x.level == condition.level for x in getattr(self.inventory, prop)))

    def test_debit_transation(self):
        self.inventory.apply_transaction("CR INV 5 X8")
        self.assertEqual(len(self.inventory.bursters), 5)

        transaction = "DR INV 3 X8"
        self.inventory.apply_transaction(transaction)
        self.assertEqual(len(self.inventory.bursters), 2)
        self.assertTrue(all(x.level == 8 for x in self.inventory.bursters))

    def test_debit_guid_transaction(self):
        for guid in ("AABBAABB", "9FD860A1"):
            # Add a Capsule with a GUID
            capsule = Inventory.Capsule()
            capsule.guid = guid
            self.inventory.add(capsule)
        transaction = "CR 9FD860A1 5 X8"
        self.inventory.apply_transaction(transaction)
        self.assertTrue(all(x.level == 8 for x in self.inventory.capsules["9FD860A1"]))
        self.assertEqual(len(self.inventory.capsules["9FD860A1"].bursters), 5)

        transaction = "DR 9FD860A1 3 X8"
        self.inventory.apply_transaction(transaction)
        self.assertTrue(all(x.level == 8 for x in self.inventory.capsules["9FD860A1"]))
        self.assertEqual(len(self.inventory.capsules["9FD860A1"].bursters), 2)
        self.assertEqual(len(self.inventory.capsules["AABBAABB"].bursters), 0)

    def test_debit_key_transaction(self):
        guid = "9FD860A1"
        # Add a Capsule with a GUID
        capsule = Inventory.Capsule(guid)
        self.inventory.add(capsule)
        transaction = (
            "CR 9FD860A1 "
            "KEY[\'Tri Bench Sculpture\' <069ea474db4947f8bed7457040b850fb.16>] "
            "KEY[\'Whiteley Walks\' <563a7d51be134cb4b5f0c3ae65912a9e.16>] "
            "KEY[\'Whiteley Walks\' <9949b5e0dc08434c9cc24fe9e499e910.16>] "
            "KEY[\'Whiteley Walks Round Coppice\' <cfce7949be3f41b9adffd383b6673752.16>]"
            "KEY[\'Winchester Miz Maze\' <>]"
        )
        self.inventory.apply_transaction(transaction)
        self.assertEqual(len(self.inventory.capsules["9FD860A1"].keys), 5)

        transaction = "DR 9FD860A1 3 KEY"
        self.inventory.apply_transaction(transaction)
        self.assertEqual(len(self.inventory.capsules["9FD860A1"].keys), 2)

    def test_stored_transaction(self):
        inventory = self.inventory
        capsule = Inventory.Capsule()
        capsule.guid = "9FD860A1"
        inventory.add(capsule)
        inventory.apply_transaction("CR INV 5 X8 10 R1")
        inventory.apply_transaction("CR 9FD860A1 10 X8")
        inventory.stage_transaction("DR INV 5 X8")
        inventory.stage_transaction("CR 9FD860A1 5 X8")
        self.assertEqual(10, len(inventory.resonators))
        self.assertEqual(5, len(inventory.bursters))
        self.assertEqual(10, len(inventory.capsules["9FD860A1"].bursters))

        inventory.apply_staged_transactions()
        self.assertEqual(10, len(inventory.resonators))
        self.assertEqual(0, len(inventory.bursters))
        self.assertEqual(15, len(inventory.capsules["9FD860A1"].bursters))

    def test_common_shield_transaction(self):
        inventory = self.inventory
        inventory.apply_transaction("CR INV 1 CS")
        self.assertEqual(1, len(inventory.shields))
        self.assertIsInstance(inventory.shields[0].rarity, Inventory.Common)

    def test_two_bursters(self):
        b1 = Inventory.Burster()
        b1.level = 8
        b2 = Inventory.Burster()
        b2.level = 8
        self.assertTrue(b1 == b2)

        b2.level = 7
        self.assertFalse(b1 == b2)

    def test_two_shields(self):
        s1 = Inventory.Shield()
        s1.rarity = Inventory.Rare()
        s2 = Inventory.Shield()
        # with when.they_are_the_same_rarity:
        s2.rarity = Inventory.Rare()
        self.assertTrue(s1 == s2)

        # with when.they_are_different_rarity:
        s2.rarity = Inventory.VeryRare()
        self.assertFalse(s1 == s2)

