import gspread
from gspread import Client, Spreadsheet, Worksheet
from typing import List, Dict
from collections import Counter



SPREADHEET_URL_TWO = 'https://docs.google.com/spreadsheets/d/1P5ZgCDnWUL_v8KV7QLxJ_Vn872ZlfWsb4J1HLfVsrTo/edit?usp=sharing'

def group_string(win: Dict) -> Dict:
    " Функция формирует новый словарь и отбрасывает ненужные данные "
    new_win: Dict = dict()
    win.pop(None)
    for k, v in win.items():
        if k.startswith('бывший штат'):
            if 'Бывший штат' in new_win:
                new_win['Бывший штат'] += 1
            else:
                new_win['Бывший штат'] = 1
        else:
            new_win[k] = v
    return new_win


def data_control(table_date: List, data: str) -> bool:
    " Функция сравнивает дату в таблице с акктуальной "
    for i in table_date:
        if data == i[:8]:
            return True


def counting(min_i: int, max_i: int, ws: Worksheet) -> Dict:
    win: List = []
    for i in range(min_i + 1, max_i):
        win.append(ws.cell(i, 10).value) # Добавляем все значения из столбца между min/max индексом
    new_win: Dict = group_string(win=Counter(win))
    return new_win


def main():
    """
    Подключение к таблице и основной код

    :return: str
    """
    gc: Client = gspread.service_account('./acount_server.json')
    sh: Spreadsheet = gc.open_by_url(SPREADHEET_URL_TWO)
    ws: Worksheet = sh.worksheet('Лист7')

    min_index: int = 0
    max_index: int = 0
    data: str = '18.02.25'
    count: int = 0

    for i in ws.col_values(10):
        count += 1
        if i == '' and count > 5:
            if data_control(table_date=ws.row_values(count), data=data): # Проверяем дату на свопадение с текущей
                if min_index == 0:
                    min_index = count
            else:
                max_index = count
                continue
    new_win: Dict = counting(min_i=min_index, max_i=max_index, ws=ws)
    return (
            f'Масс подбор на {data}\n'
            f'    -OK: {new_win.get('ок', 0)}\n    -Бывший штат: {new_win.get('Бывший штат')}\n'
            f'    -Отказ: {new_win.get('отказ', 0)}\n    -Отказ АУТ: {new_win.get('отказ аутсорс', 0)}'
    )


if __name__ == '__main__':
    main()