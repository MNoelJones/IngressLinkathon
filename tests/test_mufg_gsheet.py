"""test_mufg_gsheet.py"""
import re
from unittest import TestCase
from mufg_gsheet import MUFG_Gsheet
from Inventory import Inventory, MUFG, Capsule, Key, KeyCapsule


class TestMUFGGsheet(TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.mufg_sht = MUFG_Gsheet(
            # creds_file='/home/mnj/Downloads/IngressLinkathon-a66875a48d53.json'
        )

    def test_populate_inventory(self):
        inv_colnum = self.mufg_sht.mufg.get_int_addr("F1")[1]
        tx = self.mufg_sht.get_init_transaction_from_column(inv_colnum)
        self.inv.apply_transaction(tx)
        self.assertEqual(
            self.inv.itemcount(),
            int(self.mufg_sht.mufg.cell(*self.mufg_sht.mufg.get_int_addr("F4")).value)
        )

    def test_populate_mufgs(self):
        mufg_sht = self.mufg_sht
        inv = self.inv
        mufgs = mufg_sht.get_mufg_guids()
        for colnum, guid in mufgs:
            tx = mufg_sht.get_init_transaction_from_column(colnum, target=guid)
            print "Adding MUFG with guid {}, contents: {}".format(guid, tx)
            inv.add(MUFG(guid))
            inv.apply_transaction(tx)
        for colnum, guid in mufgs:
            print guid,
            if len(inv.mufgs[guid]):
                print ", ".join(
                    str(x) for x in inv.mufgs[guid].contents
                )
            else:
                print "Empty."
            print "itemcount {} == sheet count {}".format(
                inv.mufgs[guid].itemcount(),
                int(mufg_sht.mufg.cell(4, colnum).value)
            )
            self.assertEqual(
                inv.mufgs[guid].itemcount(),
                int(mufg_sht.mufg.cell(4, colnum).value)
            )

    def test_populate_capsules(self):
        caps = self.mufg_sht.get_capsule_guids()
        for colnum, guid in caps:
            tx = self.mufg_sht.get_init_transaction_from_column(colnum, target=guid)
            self.inv.add(Capsule(guid))
            self.inv.apply_transaction(tx)
            print "Adding Capsule with guid {}, contents: {}".format(guid, tx)
        for colnum, guid in caps:
            print guid,
            if len(self.inv.capsules[guid]):
                print ", ".join(
                    str(x) for x in self.inv.capsules[guid].contents
                )
            else:
                print "Empty."
            self.assertEqual(
                self.inv.capsules[guid].itemcount(),
                int(self.mufg_sht.mufg.cell(4, colnum).value)
            )

    def test_populate_keycapsules(self):
        caps = self.mufg_sht.get_keycap_guids()
        for colnum, guid in caps:
            tx = self.mufg_sht.get_init_transaction_from_column(colnum, target=guid)
            self.inv.add(KeyCapsule(guid))
            self.inv.apply_transaction(tx)
            print "Adding Capsule with guid {}, contents: {}".format(guid, tx)
        for colnum, guid in caps:
            print guid,
            if len(self.inv.keycaps[guid]):
                print ", ".join(
                    str(x) for x in self.inv.keycaps[guid].contents
                )
            else:
                print "Empty."
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
            print("{} [{}] (@{}, {})").format(
                k.guid or "MISSING GUID",
                k.title,
                "UNK" if not k.latlng else k.latlng["lat"],
                "UNK" if not k.latlng else k.latlng["lng"]
            )

    def test_populate_keylocker_keys(self):
        caps = self.mufg_sht.get_keycap_guids()
        for colnum, guid in caps:
            key_col = self.mufg_sht.keys.find(re.compile(guid)).col

            rng_addr = "{}:{}".format(
                self.mufg_sht.keys.get_addr_int(self.mufg_sht.key_rows_start_end[0], key_col),
                self.mufg_sht.keys.get_addr_int(self.mufg_sht.key_rows_start_end[1], key_col)
            )

            rng = self.mufg_sht.keys.range(rng_addr)
            values = [
                Key(portal=p[1])
                for p, x in zip(self.mufg_sht.portal_list, rng)
                if x.value is not None and x.value != '0'
            ]
            keycount = len(values)
            self.assertEqual(int(self.mufg_sht.keys.cell(3, key_col).value), keycount)
            print [str(v) for v in values]
