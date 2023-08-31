import os

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook


def add_data_to_excel(data, title):
    workbook = load_workbook(f'{title}.xlsx')
    sheet = workbook.active

    for row in data:
        sheet.append(row)

    workbook.save(f'{title}.xlsx')


def create_excel(category):
    path = os.path.join(os.path.dirname(__file__), f'{category}.xlsx')
    if not os.path.exists(path):
        wb = Workbook()
        ws = wb.active
        ws['A1'] = 'Название'
        ws['B1'] = 'Автор'
        ws['C1'] = 'Жанры'
        ws['D1'] = 'Теги'
        ws['E1'] = 'Цена'
        ws['F1'] = 'Просмотры'
        ws['G1'] = 'Лайки'
        ws['H1'] = 'Награды'

        wb.save(f'{category}.xlsx')
