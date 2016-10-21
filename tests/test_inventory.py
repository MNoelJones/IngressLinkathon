"""Inventory BDD Tests."""
from unittest import TestCase
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
        inventory = Inventory.Inventory()
        counts = {
            "Resonator": 10,
            "Mod": 5
        }
        for item, num in counts.iteritems():
            for _ in range(0, num):
                inventory.add(getattr(Inventory, item)())

    def test_item_count(self):
        """ With the above initialisation, invenetory count must be 15."""
        self.assertEqual(self.inventory.itemcount(), 15)

    def test_resonator_count(self):
        """ ...and the resonator count should be 10."""
        count = reduce(lambda a, b: a+b.invcount(), inventory.resonators, 0)
        self.assertEqual(count, 10)

    def test_mod_count(self):
        """ ...and the mod count should be 5."""
        count = reduce(lambda a, b: a+b.invcount(), inventory.mods, 0)
        self.assertEqual(count, 5)

    def test_immediate_count(self):
        self.assertEqual(inventory.invcount(), 15)

    def test_capsule_addition(self):
        """Adding a capsule with 5 items should make both item and inventory counts equal 21."""
        capsule = Inventory.Capsule()
        for _ in range(0, 5):
            capsule.add(Inventory.Resonator())
        self.inventory.add(capsule)

        self.assertEqual(self.inventory.itemcount(), 21)
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

        self.assertEqual(self.inventory.itemcount(), 21)
        self.assertEqual(self.inventory.invcount(), 16)
