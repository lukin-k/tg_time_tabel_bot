import requests
import datetime


class time_table:
    def __init__(self, url):
        self.time_table=[]
        self.url=url

    def lesson(self, table):
        def start_end(table):
            s=table.find('>')+1
            e=table.find('<',s)
            self.time_table.append(table[s:e])
            return e

        def pass_word(table, word, i):
            k=0
            while i:
                k=table.find(word, k)+1
                i-=1
            return k
        k=table.find('lesson__time')
        if k>=0:
            k=table.find('<span',k)
            self.time_table.append('c ')
            k+=start_end(table[k:])#time s
            k+=pass_word(table[k:], '<span', 2)
            self.time_table.append(' до ')
            k+=start_end(table[k:])#time e
            k+=pass_word(table[k:], '<span', 2)
            self.time_table.append(' ')
            k+=start_end(table[k:])#subj
        k=table.find('lesson__type',k)
        if k>=0:
            self.time_table.append('\n')
            k+=start_end(table[k:])#type
        k=table.find('lesson__teachers',k)
        if k>=0:
            k+=pass_word(table[k:], '<span', 3)
            self.time_table.append('\n')
            k+=start_end(table[k:])#teacher
        k=table.find('lesson__places',k)
        if k>=0:
            k=table.find('<a',k)
            k+=pass_word(table[k:], '<span', 2)
            self.time_table.append('\n')
            k+=start_end(table[k:])#place
            k=table.find('>ауд.',k)
            self.time_table.append(', ')
            k+=start_end(table[k:])#aud
            k=table.find('<span',k)
            self.time_table.append(' ')
            k+=start_end(table[k:])#numb
        self.time_table.append('\n-------\n')

    def get_table(self, day):
        table=requests.get(self.url).text
        s=table.find(day)
        e=table.find('</ul>', s)
        return table[s:e]

    def get_weekday(self, k):
        weekday=('пн','вт','ср','чт','пт','сб','вс')
        if k in weekday:
            return k            
        weekday_d=('понедельни','вторни','сред','четвер','пятниц','суббот','воскресени')
        if k[:-1] in weekday_d:
            return  weekday[weekday_d.index(k[:-1])]
        if len(k)>1 or not(ord(k)>=ord('0') and ord(k)<=ord('9')):
            k='0'
        l=datetime.datetime.now().weekday()+int(k)
        if l>6:
            l=6
        return weekday[l]

    def get_time_table(self, day=''):
        k='0'
        if day==' на завтра':
            k='1'
        elif day==' на послезавтра':
            k='2'
        elif day.find(' на ')==0:
            k=day[4:]
        table=self.get_table(self.get_weekday(k))
        s=table.find('<li')
        while s>=0:
            e=table.find('</li>',s)
            self.lesson(table[s:e])
            s=table.find('<li',e)
        s_time_table=''
        for i in range(len(self.time_table)):
            s_time_table+=self.time_table[i]
        self.time_table.clear()
        return s_time_table

if __name__ == '__main__':
    t=time_table('http://ruz.spbstu.ru/faculty/95/groups/24058')
    print(t.get_time_table())
