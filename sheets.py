import gspread
from gspread import Client, Spreadsheet, Worksheet
from typing import List, Any
from datetime import datetime, timedelta

SPREADHEET_URL = 'https://docs.google.com/spreadsheets/d/1CgCxgHhJj0zAwJocjJ200QFCansuJGOuQtp2P3W5_uY/edit?gid=390177914#gid=390177914'


def for_table(key: List, val: List) -> Any:
    data1: List = [(datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y'),
                   (datetime.now() - timedelta(days=1)).strftime('%d.%m.%y')]
    for i in key:
        if i == data1[0] or i == data1[1]:
            return val[key.index(i)]
    return '0'

def main():
    # Сводная таблица, выводит нарушения всех отделов по актуальной дате

    # подключение к таблице
    gc: Client = gspread.service_account('./acount_server.json')
    sh: Spreadsheet = gc.open_by_url(SPREADHEET_URL)
    ws: Worksheet = sh.worksheet('Нарушения')

    new_string = []
    # Нарушения столовая
    dining_key: List = ws.col_values(5)
    dining_val: List = ws.col_values(6)
    # Нарушения штат
    the_state_key: List = ws.col_values(1)
    the_state_val: List = ws.col_values(2)
    # Нарушения ТС
    car_key: List = ws.col_values(7)
    car_val: List = ws.col_values(8)
    # Нарушения АУТ
    ayt_key: List = ws.col_values(3)
    ayt_val: List = ws.col_values(4)



    new_string.append(for_table(dining_key, dining_val))
    new_string.append(for_table(the_state_key, the_state_val))
    new_string.append(for_table(car_key, car_val))
    new_string.append(for_table(ayt_key, ayt_val))
    return (f'Нарушения: {(datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')}\n'
            f'    -Столовая: {new_string[0]}\n    -Штат: {new_string[1]}\n'
            f'    -ТС: {new_string[2]}\n    -АУТ: {new_string[3]}')


if __name__ == '__main__':
    main()