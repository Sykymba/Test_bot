import gspread
from gspread import Client, Spreadsheet, Worksheet
from typing import List, Any

SPREADHEET_URL = 'https://docs.google.com/spreadsheets/d/1rOKB7L5nGfKr_-cF6vrr2Sf8q_DpQoM8ArSOni0Z9r0/edit?gid=1769518920#gid=1769518920'


def for_table(key: List, val: List, data: str) -> Any:
        for i in key:
            if i == data:
                return val[key.index(i)]
        return '0'

def main():
    # ------------сводная таблица, ждем решения--------------------

    gc: Client = gspread.service_account('./acount_server.json')
    sh: Spreadsheet = gc.open_by_url(SPREADHEET_URL)
    ws: Worksheet = sh.worksheet('Лист6')

    data = '19.02.2025'
    new_string = []
    # Нарушения столовая
    dining_key: List = ws.col_values(1)
    dining_val: List = ws.col_values(2)
    # Нарушения штат
    the_state_key: List = ws.col_values(3)
    the_state_val: List = ws.col_values(4)
    # Нарушения ТС
    car_key: List = ws.col_values(5)
    car_val: List = ws.col_values(6)
    # Нарушения АУТ
    ayt_key: List = ws.col_values(7)
    ayt_val: List = ws.col_values(8)



    new_string.append(for_table(dining_key, dining_val, data))
    new_string.append(for_table(the_state_key, the_state_val, data))
    new_string.append(for_table(car_key, car_val, data))
    new_string.append(for_table(ayt_key, ayt_val, data))
    return (f'Нарушения за {data}\n'
            f'    -Столовая: {new_string[0]}\n    -Штат: {new_string[1]}\n'
            f'    -ТС: {new_string[2]}\n    -АУТ: {new_string[3]}')


if __name__ == '__main__':
    main()