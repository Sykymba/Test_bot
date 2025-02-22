import gspread
from gspread import Client, Spreadsheet, Worksheet
import requests
from datetime import datetime, timedelta
from typing import List


SPREADHEET_URL = 'https://docs.google.com/spreadsheets/d/1rOKB7L5nGfKr_-cF6vrr2Sf8q_DpQoM8ArSOni0Z9r0/edit?gid=1769518920#gid=1769518920'


gc: Client = gspread.service_account('./acount_server.json')
sh: Spreadsheet = gc.open_by_url(SPREADHEET_URL)
ws = sh.worksheet('Лист6')
print(ws.row_values(1))