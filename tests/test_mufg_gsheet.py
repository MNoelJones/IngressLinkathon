"""test_mufg_gsheet.py"""
import re
from unittest import TestCase
from mufg_gsheet import MUFG_Gsheet
from Inventory import Inventory, MUFG, Capsule, Key


class TestMUFGGsheet(TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.mufg_sht = MUFG_Gsheet()

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
            # m = re.search(r"(\d+) KEY", tx)
            # if m:
            #     print "Adding {} keys.".format(m.group(1))
            #     for _ in range(int(m.group(1))):
            #         inv.mufgs[guid].add(Key())
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
