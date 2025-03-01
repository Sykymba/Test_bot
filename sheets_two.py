import gspread
from gspread import Client, Spreadsheet, Worksheet
from typing import List, Dict
from collections import Counter
from datetime import datetime, timedelta

SPREADHEET_URL_TWO = 'https://docs.google.com/spreadsheets/d/1CgCxgHhJj0zAwJocjJ200QFCansuJGOuQtp2P3W5_uY/edit?gid=390177914#gid=390177914'

def group_string(win: dict) -> Dict:
    " Функция формирует новый словарь и отбрасывает ненужные данные "
    new: Dict = dict()
    for k, v in win.items():
        if k.startswith('бывший штат'):
            if 'Бывший штат' in new:
                new['Бывший штат'] += 1
            else:
                new['Бывший штат'] = 1
        else:
            new[k] = v
    return new

def data_control(table_date: str, data) -> bool:
    " Функция сравнивает дату в таблице с акктуальной "
    control = table_date.split()
    try:
        if (control[0] == data[0] or control[0] == data[1] or control[0] == data[2]
                or control[0] == data[3] or control[0] == data[4] or control[0] == data[5]):
            return True
    except:
        return False

def processing(my_list, min_index, max_index, count, data, err_data, name):
    for i in my_list[1]:
        if i == '':
            if data_control(my_list[0][count], data):
                if min_index == 0:
                    min_index = count
            elif data_control(my_list[0][count], err_data):
                max_index = count
                break
        count += 1
        max_index = count


    win_dict: dict = dict(Counter([i
        for i in my_list[1][min_index:max_index]
                       if i != ''
    ]))

    new_win = group_string(win=win_dict)

    return (
            f'{name}: {data[0]}\n'
            f'    -OK: {new_win.get('ок', 0)}\n    -Бывший штат: {new_win.get('Бывший штат', 0)}\n'
            f'    -Отказ: {new_win.get('отказ', 0)}\n    -Отказ АУТ: {new_win.get('отказ аутсорс', 0)}\n'
            f'    -Курьер: {new_win.get('действующий курьер', 0)}'
    )

def main():
    """
    Подключение к таблице и основной код

    :return: str
    """
    gc: Client = gspread.service_account('./acount_server.json')
    sh: Spreadsheet = gc.open_by_url(SPREADHEET_URL_TWO)
    ws: Worksheet = sh.worksheet('Проверки СБ')

    name = 'Масс подбор'
    name2 = 'Точечный подбор'
    min_index: int = 0
    max_index: int = 0
    data: List = [(datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y'),
                   (datetime.now() - timedelta(days=1)).strftime('%d.%m.%y')]
    err_data: List = [datetime.now().strftime('%d.%m.%Y'), datetime.now().strftime('%d.%m.%y'),
                      (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y'),
                      (datetime.now() + timedelta(days=1)).strftime('%d.%m.%y'),
                      (datetime.now() + timedelta(days=2)).strftime('%d.%m.%Y'),
                      (datetime.now() + timedelta(days=2)).strftime('%d.%m.%y')
                      ]
    count: int = 0
    my_list: List = [ws.col_values(1), ws.col_values(2)]
    my_list2: List = [ws.col_values(3), ws.col_values(4)]


    result = processing(my_list=my_list, min_index=min_index, max_index=max_index,data=data, err_data=err_data, count=count, name=name)
    result2 = processing(my_list=my_list2, min_index=min_index, max_index=max_index,data=data, err_data=err_data, count=count, name=name2)
    finish = result + '\n\n' + result2
    return finish

if __name__ == '__main__':
    main()
