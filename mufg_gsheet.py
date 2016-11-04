import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
        self.init()

    def init(self):
        self.gc = gspread.authorize(self.creds)
        self.sht = self.gc.open("MUFG Contents")
        self.mufg = self.sht.worksheet('Sheet1')
        self.keys = self.sht.worksheet('Sheet7')

    def get_zipped_col(self, col):
        return zip(
            self.mufg.col_values(1)[:57],
            self.mufg.col_values(ord(col) - ord('A') + 1)[:57]
        )

 # "CR INV " + " ".join(["{} {}".format(x[1], x[0]) for x in mufg_sht.get_zipped_col('F')[4:] if x[1] not in ('', '0', None)])


# r = wks.range('L2:X2')
# [x.value for x in r]
# wks.col_values('L')
# wks.col_values(12)
# wks.col_values(1)[:57]
