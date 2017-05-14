import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
from collections import namedtuple
from Inventory import Portal, Key
from kids.cache import cache


class MUFG_Gsheet(object):
    def __init__(self, creds_file=None):
        scope = ["https://spreadsheets.google.com/feeds"]
        if creds_file is None:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(
                '/cygdrive/c/Users/michael.noel_jones/Downloads/IngressLinkathon-a70381e6ff09.json',
                scope
            )
        else:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        self.gc = None
        self.sht = None
        self.mufg = None
        self.keys = None
        self.min_row_loc = (1, 9)
        self.max_row_loc = (2, 9)
        self.keycap_cols_start_end = ("G", "K")
        self.mufg_cols_start_end = ("L", "X")
        self.cap_cols_start_end = ("Z", "AT")
        self.data_rows_start_end = (4, 56)
        self.extra_keys_row = 60
        self.key_rows_start_end = [None, None]
        self._portal_list = None
        self.init()

    def init(self):
        self.gc = gspread.authorize(self.creds)
        self.sht = self.gc.open("MUFG2")
        self.mufg = self.sht.worksheet('Inventory')
        self.keys = self.sht.worksheet('Keys')
        MUFG_Gsheet.MufgTuple = namedtuple(
            "MufgTuple",
            self._data_values(1)
        )
        self.key_rows_start_end[0] = int(self.keys.cell(*self.min_row_loc).value)
        self.key_rows_start_end[1] = int(self.keys.cell(*self.max_row_loc).value)

    @property
    def portal_list(self):
        if self._portal_list is None:
            self._portal_list = self.get_portal_list()
        return self._portal_list

    def refresh_portal_list(self):
        self._portal_list = None
        return self.portal_list

    def _data_values(self, col_num):
        return self.mufg.col_values(col_num)[
            self.data_rows_start_end[0]:
            self.data_rows_start_end[1]
        ]

    @cache
    def get_colnum_data(self, col_number):
        return MUFG_Gsheet.MufgTuple._make(self._data_values(col_number))

    @cache
    def get_colname_data(self, col_name):
        return MUFG_Gsheet.MufgTuple._make(self._data_values(self.mufg.get_int_addr(col_name + "1")[1]))

    @cache
    def get_mufg_guids(self):
        return [(x.col, x.value) for x in self.mufg.range("{}2:{}2".format(*self.mufg_cols_start_end))]

    @cache
    def get_keycap_guids(self):
        rng = self.mufg.range("{}2:{}2".format(*self.keycap_cols_start_end))
        guids = [(x.col, x.value.split(" ")[1]) for x in rng]
        return guids

    @cache
    def get_capsule_guids(self):
        rng = self.mufg.range("{}2:{}2".format(*self.cap_cols_start_end))
        return [(x.col, x.value) for x in rng]

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

    def get_portal_list(self):
        key_info = {
            "title": 1,
            "note": 2,
            "latlng": {"lat": 3, "lng": 4},
            "guid": 5,
            "area": 8,
        }
        portal_list = []
        portal_data = self.keys.range(
            self.keys.get_addr_int(self.key_rows_start_end[0], 1) +
            ":" +
            self.keys.get_addr_int(self.key_rows_start_end[1], 8)
        )
        portal_info = [
            portal_data[i:i + 8]
            for i in range(0, len(portal_data), 8)
        ]
        for vals in portal_info:
            d = {
                prop: vals[col - 1].value
                for prop, col in key_info.iteritems()
                if prop != "latlng"
            }
            latlng = self.gen_lat_lng_from_strings((
                vals[key_info["latlng"]["lat"] - 1].value,
                vals[key_info["latlng"]["lng"] - 1].value
            ))
            d["latlng"] = latlng
            p = Portal(**d)
            k = Key(portal=p)
            portal_list.append((vals[0].row, k))
        return portal_list

    def get_init_transaction_from_column(self, target="INV"):
        col_number = self.get_col_for_target("mufg", target)
        col_vals = self.get_colnum_data(col_number)
        extra_key_tx = self.get_extra_key_transaction(target)
        tx = (
            "CR {} ".format(target) +
            " ".join(
                [
                    "{} {}".format(count, name)
                    for name, count in col_vals._asdict().iteritems()
                    if count not in ('', '0', None) and name not in "Keys"
                ] +
                self.get_key_transaction(target) +
                extra_key_tx["CR"]
            )
        )
        if "DR" in extra_key_tx:
            tx += (
                " " +
                "DR {}".format(target) +
                " ".join(extra_key_tx["DR"])
            )
        return tx

    #@cache
    def get_col_for_target(self, sheet="mufg", target="INV"):
        sheet_target_locations = {
            "mufg": "F2:AT2",
            "keys": "J4:AZ4"
        }
        targets = getattr(self, sheet).range(sheet_target_locations[sheet])
        c = re.compile(target, re.IGNORECASE)
        try:
            return [t for t in targets if c.search(t.value)][0].col
        except IndexError as err:
            raise Exception(
                "Cannot find column for target "
                "{} in {} ({})".format(target, sheet, err)
            )

    def get_keys(self, target):
        key_col = self.get_col_for_target("keys", target)

        rng_addr = "{}:{}".format(
            self.keys.get_addr_int(self.key_rows_start_end[0], key_col),
            self.keys.get_addr_int(self.key_rows_start_end[1], key_col)
        )

        rng = self.keys.range(rng_addr)
        values = []
        for p, x in zip(self.portal_list, rng):
            if bool(x.value) and int(x.value) is not 0:
                values.extend([Key(portal=p[1]) for _ in range(int(x.value))])
        return values

    def get_key_transaction(self, target):
        values = self.get_keys(target)
        return [str(val) for val in values]

    def get_extra_key_transaction(self, target):
        extra_keys = self.translate_string_to_value(
            self.mufg.cell(
                self.extra_keys_row,
                self.get_col_for_target(target=target)
            ).value,
            none_is_zero=True
        )
        ret = {"CR": [], "DR": []}
        if extra_keys > 0:
            ret["CR"] = ["{} KEY".format(extra_keys)]
        elif extra_keys < 0:
            ret["DR"] = ["{} KEY".format(-extra_keys)]
        return ret

    def translate_string_to_value(self, instr, none_is_zero=False):
        if instr == "":
            return 0 if none_is_zero else None
        return int(instr)


# "CR INV " + " ".join(["{} {}".format(x[1], x[0]) for x in mufg_sht.get_zipped_col('F')[4:] if x[1] not in ('', '0', None)])


def main():
    from Inventory import Inventory, MUFG, Capsule

    inv = Inventory()
    mufg_sht = MUFG_Gsheet()
    inv_colnum = mufg_sht.mufg.get_int_addr("F1")[1]
    tx = mufg_sht.get_init_transaction_from_column(inv_colnum)
    inv.apply_transaction(tx)

    mufgs = mufg_sht.get_mufg_guids()
    for colnum, guid in mufgs:
        tx = mufg_sht.get_init_transaction_from_column(colnum, target=guid)
        inv.add(MUFG(guid))
        inv.apply_transaction(tx)
    for guid in inv.mufgs:
        print ", ".join(
            "{}{}".format(
                x.shortcode,
                x.level if hasattr(x, "has_level") else ""
            )
            for x in inv.mufgs[guid].contents
        )
    caps = mufg_sht.get_capsule_guids()
    for colnum, guid in caps:
        tx = mufg_sht.get_init_transaction_from_column(colnum, target=guid)
        inv.add(Capsule(guid))
        inv.apply_transaction(tx)
    for guid in inv.capsules:
        print ", ".join(
            "{}{}{}".format(
                x.rarity if hasattr(x, "has_rarity") else "",
                x.shortcode,
                x.level if hasattr(x, "has_level") else ""
            )
            for x in inv.capsules[guid].contents
        )


# r = wks.range('L2:X2')
# [x.value for x in r]
# wks.col_values('L')
# wks.col_values(12)
# wks.col_values(1)[:57]
