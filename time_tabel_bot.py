import bot
import time_tabel
import datetime

token='486794750:AAH2ltgRjCk__ZCtPcGySPwL9dPio63Ez8c'
bot=bot.Bot(token)
new_offset=None

url='http://ruz.spbstu.ru/faculty/95/groups/24058'
ti_ta=time_tabel.time_table(url)

help_text='''"добавь меня в список"-подписывает вас на ежедневную рассылку расписания
"удали меня из списка" - отписывает вас от рассылки
"раписание" - печатает расписание на сегодня
"раписание на пн/понедельник/завтра" - печатает расписание на выбранный день (работаеет только в пределах данной недели)'''

bad=['гей','пидор','пидр','урод','хуй','уебок','уёбок', 'похёл на хуй', 'пошел на хуй']
id_list=[]

today = datetime.datetime.now().day

while True:
    bot.get_updates(new_offset)
    last=bot.get_last_update()
    if len(id_list)and today==datetime.datetime.now().day and 1<=datetime.datetime.now().hour<=2:
        for chat_id in id_list:
            bot.send_message(chat_id, ti_ta.get_time_table())
        today+=1
    if last:
        last_chat_id=last['message']['chat']['id']
        last_text=last['message']['text']
        if last_text.lower()[:len('расписание')] =='расписание':
            last_text=ti_ta.get_time_table(last_text.lower()[len('расписание'):])
            if last_text=='':
                last_text='Не нашёл расписание'
        elif last_text.lower()=='help':
            last_text=help_text
        elif last_text.lower() in bad:
            last_text='Сам '+last_text
        elif last_text.lower()=='добавь меня в список':
            if not (last_chat_id in id_list):
                id_list.append(last_chat_id)
                last_text='Добавил'
            else:
                last_text='Вы уже в списке'
        elif last_text.lower()=='удали меня из списка':
            if last_chat_id in id_list:
                id_list.remove(last_chat_id)
                last_text='Удалил'
            else:
                last_text='Вы не были в списке'
        bot.send_message(last_chat_id, text=last_text)
        new_offset=last['update_id']+1
