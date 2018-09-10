import re

from bs4 import BeautifulSoup

file = open('C:\\users\\anonim\\index.html', 'r', encoding='utf-8')

doc = file.read()

doc = re.sub(r'[\t\r\n]', '', doc)


doc = BeautifulSoup(''.join(doc), features='html.parser')

def parse_table(table):
    razdel = ''
    podrazdel = ''
    main_name = ''
    unit_position = list()

    all_rows = table.find_all('tr')
    for row in all_rows:
        true_rows = row.find_all('td')
        if (len(true_rows)) < 8:
            continue
        for true_row in true_rows:
            for t in true_row.find_all('span'):
                t = t.replace(' ', '')
                if t != '':
                    print(''.join(t.find(text=True)))

tables = doc.find_all('table')
for table in tables:
    trs = table.find_all('tr')
    for tr in trs:
        for text in tr.find_all(text=True):
            if ''.join(text).lower().find('Раздел'.lower()) != -1:
                parse_table(table)
                exit(0)

