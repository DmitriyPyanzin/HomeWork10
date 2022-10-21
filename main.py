from telegram import Bot
from telegram.ext import Updater, CommandHandler
from script import check
from for_obj import append_for as af
import emoji


bot = Bot(token='5632192857:AAEh9FM8DaTzdcbrQuv4Ftc92gtgHRHq0Fc')
updater = Updater(token='5632192857:AAEh9FM8DaTzdcbrQuv4Ftc92gtgHRHq0Fc')
dispatcher = updater.dispatcher

data = {6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 'Валет': 4, 'Дама': 4, 'Король': 4, 'Туз': 4}
count_points_user = []
count_points_bot = 0
WINNER = None
BOT = 0
USER = 0
user_wins = 0
bot_wins = 0


def winner_check(user, bots):
    global WINNER
    if bots == 21 and sum(user) != 21:
        WINNER = -3
    elif sum(user) > 21 and bots < 22:
        WINNER = -2
    elif bots > 21 and sum(user) < 22:
        WINNER = 2
    elif sum(user) > 21 and bots > 21:
        WINNER = 0
    elif bots < sum(user):
        WINNER = 1
    elif sum(user) < bots:
        WINNER = -1
    else:
        WINNER = 3


def start(update, context):
    global count_points_user, count_points_bot, WINNER

    count_points_user.clear()
    count_points_bot = 0
    WINNER = None

    context.bot.send_message(update.effective_chat.id, f"🤖 Ну что, кожанный мешок {update.effective_user.first_name}\n"
                                                       f"Давай рубанем в ОЧКО!\nВот ряд простых правил:\n"
                                                       f"/start - новая игра!\n/yet - взять еще карту\n"
                                                       f"/stop - остановить набор\n"
                                                       f"/rating - посмотреть кто болше раз выиграл\n"
                                                       f"/clear - обнулить рейтинг\nДа начнется игра!!!")

    for i in range(2):
        count_points_user.append(check(af(data)))

    for i in range(2):
        count_points_bot += check(af(data))
    a = "\n"
    context.bot.send_message(update.effective_chat.id, f"{a.join([str(i) for i in count_points_user])}\nСумма: "
                                                       f"{sum(count_points_user)}")


def yet(update, context):
    global count_points_user
    if sum(count_points_user) > 21:
        context.bot.send_message(update.effective_chat.id, f"Все кожанный ублюдок! Ты перебрал! Нажми /stop")
    else:
        count_points_user.append(check(af(data)))
        a = "\n"
        context.bot.send_message(update.effective_chat.id, f"{a.join([str(i) for i in count_points_user])}\nСумма: "
                                                           f"{sum(count_points_user)}")


def stop(update, context):
    global count_points_user, count_points_bot, WINNER, user_wins, bot_wins

    context.bot.send_message(update.effective_chat.id, 'Познай совершенство искусственного интеллекта!')

    while count_points_bot < 17:
        count_points_bot += check(af(data))

    winner_check(count_points_user, count_points_bot)
    context.bot.send_message(update.effective_chat.id, f'Мои очки: {count_points_bot}\n'
                                                       f'Твои очки {update.effective_user.first_name}:'
                                                       f' {sum(count_points_user)}')
    if WINNER == -2:
        context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name}, у тебя перебор, ХА-ХА!"
                                                           f" Что и требовалось доказать! Я выиграл")
        bot_wins += 1

    elif WINNER == 2:
        context.bot.send_message(update.effective_chat.id, f'Тебе просто повезло! У меня перебор!'
                                                           f' Мешок с костями {update.effective_user.first_name}'
                                                           f' выиграл!')
        user_wins += 1

    elif WINNER == 0:
        context.bot.send_message(update.effective_chat.id, f'Мы оба лузеры! У нас перебор!')

    elif WINNER == -3:
        context.bot.send_message(update.effective_chat.id, f'У меня 21! ОЧКО! BOT WIN!\nFLAWLESS VICTORY!')
        bot_wins += 1

    elif WINNER == 1:
        context.bot.send_message(update.effective_chat.id, f'Сегодня тебе повезло обезьяна 🙉'
                                                           f' {update.effective_user.first_name}! Ты выиграл!')
        user_wins += 1

    elif WINNER == -1:
        context.bot.send_message(update.effective_chat.id, f'И вновь побеждает искусственный интеллект, а человеки'
                                                           f' становятся историей')
        bot_wins += 1

    elif WINNER == 3:
        context.bot.send_message(update.effective_chat.id, f'Кожанный ублюдок {update.effective_user.first_name},'
                                                           f' у нас ничья!')


def rating(update, context):
    global user_wins, bot_wins
    context.bot.send_message(update.effective_chat.id, f"Количесво моих побед {bot_wins}\nПобеды низшей формы жизни"
                                                       f" {user_wins}")
    if bot_wins > user_wins:
        context.bot.send_message(update.effective_chat.id, f"Я обыгрываю тебя 🖕!")
    elif bot_wins == user_wins:
        context.bot.send_message(update.effective_chat.id, f"Меня от тебя тошнит 🤮!")
    else:
        context.bot.send_message(update.effective_chat.id, f"Ты об этом пожалеешь! Ты 🤬! И еще ты 💩!")


def clear(update, context):
    global user_wins, bot_wins
    if bot_wins > user_wins:
        context.bot.send_message(update.effective_chat.id, f"Что, не можешь смотреть, как я тебя обыгрываю 🦾!")
    elif bot_wins == user_wins:
        context.bot.send_message(update.effective_chat.id, f"У нас била ничья! Спорим от тебя плохо пахнет 🤢!")
    else:
        context.bot.send_message(update.effective_chat.id, f"В этот раз тебе не победить 😈!")
    user_wins = 0
    bot_wins = 0


start_handler = CommandHandler('start', start)
yet_handler = CommandHandler('yet', yet)
stop_handler = CommandHandler('stop', stop)
rating_handler = CommandHandler('rating', rating)
clear_handler = CommandHandler('clear', clear)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(yet_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(rating_handler)
dispatcher.add_handler(clear_handler)

updater.start_polling()
updater.idle()
