"""Googlesheets module"""

import gspread
import gspread_formatting
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsData():
    """Class for google sheets handling"""

    def __init__(self):
        """Initiating - authentication"""
        self.scope = ["https://spreadsheets.google.com/feeds",
                      "https://www.googleapis.com/auth/spreadsheets",
                      "https://www.googleapis.com/auth/drive.file",
                      "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            "API_creds.json", self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open('Amazon_Stats').sheet1
        gspread_formatting.set_row_height(self.sheet, '2:100000', 150)
        gspread_formatting.set_column_width(self.sheet, 'A:G', 150)

    def insert_data_row(self, data):
        """Insert row into sheet"""
        if data:
            self.sheet.insert_row(data, 2, value_input_option='USER_ENTERED' )
        else:
            pass

    def insert_data(self, row, col, data):
        """Insert value to cell"""
        self.sheet.update_cell(row, col, data)

    def read_data(self, row, col):
        """Read value from cell"""
        value = self.sheet.cell(row, col).value
        return value

    def how_long_col(self, col):
        """Get column length"""
        length = len(self.sheet.col_values(col))
        return length

