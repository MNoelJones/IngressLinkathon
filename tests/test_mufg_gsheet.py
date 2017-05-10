"""test_mufg_gsheet.py."""
from unittest import TestCase
from mufg_gsheet import MUFG_Gsheet
from Inventory import Inventory, MUFG, Capsule, Key, KeyCapsule


class TestMUFGGsheet(TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.mufg_sht = MUFG_Gsheet(
            # creds_file='IngressLinkathon-5dbf4501bc77.json'
            # creds_file='/home/mnj/Downloads/IngressLinkathon-0bfda0130198.json'
            creds_file='/home/mnj/Downloads/IngressLinkathon-a66875a48d53.json'
        )

    def test_populate_inventory(self):
        """ Populate mufg instance from INV column """
        tx = self.mufg_sht.get_init_transaction_from_column("INV")
        print(tx)
        self.inv.apply_transaction(tx)
        self.assertEqual(
            self.inv.itemcount(),
            int(self.mufg_sht.mufg.cell(
                *self.mufg_sht.mufg.get_int_addr("F4")
            ).value)
        )

    def test_populate_mufgs(self):
        mufg_sht = self.mufg_sht
        inv = self.inv
        mufgs = mufg_sht.get_mufg_guids()
        for colnum, guid in mufgs:
            tx = mufg_sht.get_init_transaction_from_column(target=guid)
            inv.add(MUFG(guid))
            inv.apply_transaction(tx)
        for colnum, guid in mufgs:
            self.assertEqual(
                inv.mufgs[guid].itemcount(),
                int(mufg_sht.mufg.cell(4, colnum).value)
            )

    def test_populate_capsules(self):
        caps = self.mufg_sht.get_capsule_guids()
        for colnum, guid in caps:
            tx = self.mufg_sht.get_init_transaction_from_column(
                target=guid
            )
            self.inv.add(Capsule(guid))
            self.inv.apply_transaction(tx)
        for colnum, guid in caps:
            print guid,
            self.assertEqual(
                self.inv.capsules[guid].itemcount(),
                int(self.mufg_sht.mufg.cell(4, colnum).value)
            )

    def test_populate_keycapsules(self):
        caps = self.mufg_sht.get_keycap_guids()
        for colnum, guid in caps:
            tx = self.mufg_sht.get_init_transaction_from_column(
                target=guid
            )
            self.inv.add(KeyCapsule(guid))
            self.inv.apply_transaction(tx)
        for colnum, guid in caps:
            self.assertEqual(
                self.inv.keycaps[guid].itemcount(),
                int(self.mufg_sht.mufg.cell(4, colnum).value)
            )

    def test_generate_key(self):
        portal_list = self.mufg_sht.get_portal_list()
        for row, portal in portal_list:
            vals = self.mufg_sht.keys.range(
                self.mufg_sht.keys.get_addr_int(row, 1) + ":" +
                self.mufg_sht.keys.get_addr_int(row, 8)
            )
            k = Key(portal=portal)
            self.assertEqual(k.title, vals[0].value)
            self.assertEqual(k.guid, vals[4].value)

    def test_populate_keylocker_keys(self):
        caps = self.mufg_sht.get_keycap_guids()
        for colnum, guid in caps:
            values = self.mufg_sht.get_keys(guid)
            keycount = len(values)
            cell = self.mufg_sht.keys.cell(
                3,
                self.mufg_sht.get_col_for_target(sheet="keys", target=guid)
            )
            sheet_count = self.mufg_sht.translate_string_to_value(cell.value)
            self.assertEqual(sheet_count, keycount)

    def test_find_capsules_with_key_changes(self):
        pass
