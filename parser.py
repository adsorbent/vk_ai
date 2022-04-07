import os
import re
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from bs4 import BeautifulSoup

files = {}
paths = os.listdir('messages/')
for path in paths:
    if path == 'index-messages.html':
        pass
    else:
        files.update({path: os.listdir('messages/' + path + '/')})

output = []
indexOfPath = 0
pageNum = 0


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

for i in range(len(files)):
    files[list(files.keys())[i]].sort(key=natural_keys)

def arse():
    global indexOfPath, pageNum, output

    for xyz1 in range(len(files)):
        pageNum = len(files[list(files.keys())[indexOfPath]]) - 1

        for xyz in range(len(files[list(files.keys())[indexOfPath]])):
            path = 'messages/' + list(files.keys())[indexOfPath] + '/' + files[list(files.keys())[indexOfPath]][pageNum]

            index = open(path, 'r', encoding='Windows-1251').read()

            finditDate = '/html/body/div/div[2]/div/div/div/div/div[1]'
            finditText = '/html/body/div/div[2]/div/div/div/div/div[2]'
            finditName = '/html/body/div/div[2]/h2/div/div[3]/div[3]'

            root = fromstring(index)

            date = root.xpath(finditDate)
            text = root.xpath(finditText)
            name = root.xpath(finditName)

            name = BeautifulSoup(tostring(name[0]), 'lxml').get_text()  #имя файла

            for i in range(len(date)):
                soupDate = BeautifulSoup(tostring(date[len(date) - i - 1]), 'lxml')
                dateOut = soupDate.select_one('.message__header').get_text().split(sep=',')   #дата на выход, где date[0] - отправитель, date[1] - дата
                soupText = BeautifulSoup(tostring(text[len(text) - i - 1]), 'lxml').get_text()    #само сообщение

                if soupText[
                   0:1] != '\n' and '\nФотография\n' not in soupText and '\n1 прикреплённое сообщение\n' not in soupText \
                        and 'вышел из беседы' not in soupText and 'вернулся в беседу' not in soupText and 'вышла из беседы' not in soupText \
                        and 'к беседе по ссылке' not in soupText and 'История' not in soupText and 'Ссылка' not in soupText \
                        and 'Видеозапись' not in soupText and 'Файл' not in soupText and \
                        'прикреплённых сообщения' not in soupText:

                    output.append(dateOut[0] + '":"' + soupText)

            pageNum -= 1

        outFile = open('out/' + re.sub('\W+', ' ', name) + '.txt', 'w+', encoding='utf-8')
        for i in range(0, len(output)):
            outFile.write(output[i])
        indexOfPath += 1
        pageNum = 0
        outFile.close()
        output = []
        print('created', name, indexOfPath, 'of', len(files), '//DEBUG:', list(files.keys())[indexOfPath])   #заменить print retun'om



def parse():
    global indexOfPath, pageNum

    while indexOfPath < len(files):
        try:
            arse()

        except Exception as e:
            print(e, 'happend on ', indexOfPath, ' indexOfPath and ', pageNum, ' pageNum')  #заменить print retun'om
            indexOfPath += 1
            pageNum = 0


parse()