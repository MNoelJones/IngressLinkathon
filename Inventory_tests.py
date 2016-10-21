# Inventory BDD Tests
from pyspecs import given, when, the, then, and_, however, this
import Inventory

# It should allow you to add any Item to it
with given.an_empty_inventory:
    inventory = Inventory.Inventory()
    with then.the_inventory_size_should_be_zero:
        the(inventory.invcount()).should.equal(0)

    with when.adding_a_mod:
        item = Inventory.Mod()
        inventory.add(item)

        with then.the_size_should_be_one:
            the(inventory.invcount()).should.equal(1)

if False:
    with given.an_item:
        with then.insantiating_the_Item_raises_an_error:
            the(Inventory.Item).should.raise_a(TypeError)

with given.a_populated_inventory:
    inventory = Inventory.Inventory()
    counts = {
        "Resonator": 10,
        "Mod": 5
    }
    for item, num in counts.iteritems():
        for _ in range(0, num):
            inventory.add(getattr(Inventory, item)())

    with then.inventory_count_is_15:
        the(inventory.invcount()).should.equal(15)

    with then.inventory_count_of_resonators_is_10:
        the(
            reduce(lambda a, b: a+b.invcount(), inventory.resonators, 0)
        ).should.equal(10)
    with then.inventory_count_of_mods_is_5:
        the(
            reduce(lambda a, b: a+b.invcount(), inventory.mods, 0)
        ).should.equal(5)

    with then.immediate_inventory_count_is_15:
        the(inventory.invcount()).should.equal(15)

    with when.adding_a_capsule_with_5_items:
        capsule = Inventory.Capsule()
        for _ in range(0, 5):
            capsule.add(Inventory.Resonator())
        inventory.add(capsule)

        with and_.both_counts_are_21:
            the(inventory.itemcount()).should.equal(21)
            the(inventory.invcount()).should.equal(21)

    with when.adding_a_keylocker_with_5_keys:
        locker = Inventory.KeyCapsule()
        for _ in range(0, 5):
            locker.add(Inventory.Key())
        inventory.add(locker)

        with then.itemcount_is_27:
            the(inventory.itemcount()).should.equal(27)
        with however.inventory_count_should_equal_22:
            the(inventory.invcount()).should.equal(22)

with given.a_L8_burster:
    burster = Inventory.Burster()
    burster.level = 8
    with then.the_level_should_report_8:
        the(burster.level).should.equal(8)

with given.adding_individual_item_from_processed_transaction_should_be_correct:
    inventory = Inventory.Inventory()
    transaction = "5 X8"
    operation = "add"
    target = inventory
    inventory._apply_individual_transaction(operation, target, transaction)
    with then.the_inventory_should_have_five_Bursters:
        the(len(inventory.bursters)).should.equal(5)
    with then.the_bursters_should_all_be_level_eight:
        the(all(x.level == 8 for x in inventory.bursters)).should.be(True)

with given.adding_inventory_from_a_transaction_specification_for_5_L8_Bursters:
    inventory = Inventory.Inventory()
    transaction = "CR INV 5 X8"
    inventory.apply_transaction(transaction)
    with then.the_inventory_should_have_five_Bursters:
        the(len(inventory.bursters)).should.equal(5)
    with then.the_bursters_should_all_be_level_eight:
        the(all(x.level == 8 for x in inventory.bursters)).should.be(True)

with given.adding_from_a_transaction_specification_for_multiple_items:
    inventory = Inventory.Inventory()
    transaction = "CR INV 5 X8 3 R6"
    inventory.apply_transaction(transaction)
    with and_.the_inventory_should_have_the_correct_number_of_each_item:
        the(len(inventory.bursters)).should.equal(5)
        the(len(inventory.resonators)).should.equal(3)
    with and_.the_items_should_be_the_correct_level:
        the(all(x.level == 8 for x in inventory.bursters)).should.be(True)
        the(all(x.level == 6 for x in inventory.resonators)).should.be(True)

with given.a_debit_transation:
    # Add 5 X8s so we can remove some of them
    inventory = Inventory.Inventory()
    transaction = "CR INV 5 X8"
    inventory.apply_transaction(transaction)
    with then.the_inventory_should_have_five_Bursters:
        the(len(inventory.bursters)).should.equal(5)

    # Remove 3 of the added bursters
    transaction = "DR INV 3 X8"
    inventory.apply_transaction(transaction)

    with then.the_inventory_should_have_two_Bursters:
        the(len(inventory.bursters)).should.equal(2)
    with then.the_bursters_should_all_be_level_eight:
        the(all(x.level == 8 for x in inventory.bursters)).should.be(True)

with given.a_debit_transation_for_a_guid_item:
    inventory = Inventory.Inventory()
    for guid in ("AABBAABB", "9FD860A1"):
        # Add a Capsule with a GUID
        capsule = Inventory.Capsule()
        capsule.guid = guid
        inventory.add(capsule)
    # Add 5 X8s so we can remove some of them
    transaction = "CR 9FD860A1 5 X8"
    inventory.apply_transaction(transaction)
    # Remove 3 of the added bursters
    transaction = "DR 9FD860A1 3 X8"
    inventory.apply_transaction(transaction)

    with then.the_other_capsule_should_be_empty:
        the(len(inventory.capsules["AABBAABB"])).should.equal(0)
    with then.the_targeted_capsule_should_have_two_Bursters:
        the(len(inventory.capsules["9FD860A1"])).should.equal(2)
    with then.the_bursters_should_all_be_level_eight:
        the(
            all(
                x.level == 8
                for x in inventory.capsules["9FD860A1"]
            )
        ).should.be(True)

with given.a_stored_transaction:
    inventory = Inventory.Inventory()
    capsule = Inventory.Capsule()
    capsule.guid = "9FD860A1"
    inventory.add(capsule)
    inventory.apply_transaction("CR INV 5 X8 10 R1")
    inventory.apply_transaction("CR 9FD860A1 10 X8")
    inventory.stage_transaction("DR INV 5 X8")
    inventory.stage_transaction("CR 9FD860A1 5 X8")
    with and_.the_inventory_contents_should_be_correct:
        the(len(inventory.resonators)).should.equal(10)
        the(len(inventory.bursters)).should.equal(5)
        the(len(inventory.capsules["9FD860A1"].bursters)).should.equal(10)

    with then.applying_staged_transactions:
        inventory.apply_staged_transactions()
        with and_.the_inventory_contents_should_be_correct:
            the(len(inventory.resonators)).should.equal(10)
            the(len(inventory.bursters)).should.equal(0)
            the(len(inventory.capsules["9FD860A1"].bursters)).should.equal(15)

with given.A_transaction_for_a_Common_Shield:
    inventory = Inventory.Inventory()
    inventory.apply_transaction("CR INV 1 CS")
    with and_.The_inventory_should_contain_one_Common_Shield:
        the(len(inventory.shields)).should.be(1)
        the(inventory.shields[0].rarity).should.be(Inventory.Common)

with given.two_bursters:
    b1 = Inventory.Burster()
    b1.level = 8
    b2 = Inventory.Burster()
    with when.they_are_the_same_level:
        b2.level = 8
        with then.they_should_be_considered_equal:
            this(b1 == b2).should.be(True)
    with when.they_are_different_levels:
        b2.level = 7
        with then.they_should_not_be_considered_equal:
            this(b1 == b2).should_NOT.be(True)

with given.two_shields:
    s1 = Inventory.Shield()
    s1.rarity = Inventory.Rare()
    s2 = Inventory.Shield()
    with when.they_are_the_same_rarity:
        s2.rarity = Inventory.Rare()
        this(s1 == s2).should.be(True)
    with when.they_are_different_rarity:
        s2.rarity = Inventory.VeryRare()
        this(s1 == s2).should.be(False)
