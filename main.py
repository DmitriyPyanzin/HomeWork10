from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from script import check
from random import choice as ch


bot = Bot(token='5632192857:AAEh9FM8DaTzdcbrQuv4Ftc92gtgHRHq0Fc')
updater = Updater(token='5632192857:AAEh9FM8DaTzdcbrQuv4Ftc92gtgHRHq0Fc')
dispatcher = updater.dispatcher

data = {6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 'Валет': 4, 'Дама': 4, 'Король': 4, 'Туз': 4}

count_points_user = []
count_points_bot = 0

WINNER = None

BOT = 1
USER = 2


def winner_check(user, bots):
    global WINNER
    if sum(user) > 21 and bots < 22:
        WINNER = -1
    elif bots > 21 and sum(user) < 22:
        WINNER = 1
    elif sum(user) > 21 and bots > 21:
        WINNER = 0

    if bots < sum(user) <= 21 and bots <= 21:
        WINNER = 1
    elif sum(user) < bots <= 21 and sum(user) <= 21:
        WINNER = -1
    else:
        WINNER = 0


def start(update, context):
    global count_points_user, count_points_bot, WINNER

    count_points_user.clear()
    count_points_bot = 0
    WINNER = None

    for i in range(2):
        data_object = ch(list(data.keys()))
        while data[data_object] == 0:
            data_object = ch(list(data.keys()))
        data[data_object] -= 1
        points = check(data_object)
        count_points_user.append(points)

    for i in range(2):
        data_object = ch(list(data.keys()))
        while data[data_object] == 0:
            data_object = ch(list(data.keys()))
        data[data_object] -= 1
        points = check(data_object)
        count_points_bot += points

        if sum(count_points_user) > 21 and count_points_bot < 22:
            context.bot.send_message(update.effective_chat.id, "Перебор, выиграл бот")
        elif count_points_bot > 21 and sum(count_points_user) < 22:
            context.bot.send_message(update.effective_chat.id, f"Перебор, выиграл {update.effective_user.first_name}")
        elif sum(count_points_user) > 21 and count_points_bot > 21:
            context.bot.send_message(update.effective_chat.id, "Перебор, вы лузеры")
        else:
            a = '\n'.join([str(i) for i in count_points_user])
            context.bot.send_message(update.effective_chat.id, f"{a}\nСумма:{sum(count_points_user)}")


def yet(update, context):
    global count_points_user
    if sum(count_points_user) < 21:
        data_object = ch(list(data.keys()))
        while data[data_object] == 0:
            data_object = ch(list(data.keys()))
        data[data_object] -= 1
        points = check(data_object)
        count_points_user.append(points)
        a = '\n'.join([str(i) for i in count_points_user])
        context.bot.send_message(update.effective_chat.id, f"{a}\nСумма:{sum(count_points_user)}")
    else:
        context.bot.send_message(update.effective_chat.id, f"Ты не можешь взять больше")


def stop(update, context):
    global count_points_user, count_points_bot
    if WINNER is None:
        context.bot.send_message(update.effective_chat.id, 'Вы закончили набор, Теперь набирает бот')
        while count_points_bot > 15 and ch([True, False]) or count_points_bot <= 12:
            data_object = ch(list(data.keys()))
            while data[data_object] == 0:
                data_object = ch(list(data.keys()))
            data[data_object] -= 1
            points = check(data_object)
            count_points_bot += points

        winner_check(count_points_user, count_points_bot)
        context.bot.send_message(update.effective_chat.id, f'Очки бота: {count_points_bot}\n'
                                                           f'Очки {update.effective_user.first_name}:'
                                                           f' {sum(count_points_user)}')
        if WINNER == -1:
            context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name}, у тебя перебор,"
                                                               f" выиграл бот")
        elif WINNER == 1:
            context.bot.send_message(update.effective_chat.id, f'{update.effective_user.first_name}, ты выиграл')
        elif WINNER == 0:
            context.bot.send_message(update.effective_chat.id, f'{update.effective_user.first_name} вы с ботом лузеры')
    else:
        context.bot.send_message(update.effective_chat.id, f'Игра окончена, чтобы начать заново напишите /start')


start_handler = CommandHandler('start', start)
yet_handler = CommandHandler('yet', yet)
stop_handler = CommandHandler('stop', stop)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(yet_handler)
dispatcher.add_handler(stop_handler)

updater.start_polling()
updater.idle()
