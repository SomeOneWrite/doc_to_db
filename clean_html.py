from bs4 import BeautifulSoup

file = open('C:\\index.htm', 'r')

doc = file.read()

doc = BeautifulSoup(''.join(doc), features='html.parser')

file.close()

for tag in doc():
    for attribute in ["class", "id", "name", "style"]:
        del tag[attribute]

file = open('C:\\users\\anonim\\index.html', 'w',  encoding='utf-8')

file.write(doc.prettify())

file.flush()
file.close()