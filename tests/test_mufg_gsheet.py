"""test_mufg_gsheet.py"""
from unittest import TestCase
from mufg_gsheet import MUFG_Gsheet
from Inventory import Inventory, MUFG, Capsule, Key, KeyCapsule, Portal


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

    def gen_lat_lng_from_strings(self, latlng_tpl_s):
        lat = latlng_tpl_s[0]
        lng = latlng_tpl_s[1]
        if not lat or lat == "":
            lat = 0
        if not lng or lng == "":
            lng = 0
        latlng = {
            "lat": int(lat),
            "lng": int(lng)
        }
        return latlng

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
