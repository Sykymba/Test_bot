import telebot
from TOKEN import TOKEN_BOT, CHAT_ID
from datetime import datetime
import time
import sheets
import sheets_two

class Bot:
    def __init__(self) -> None:
        self.__bot = telebot.TeleBot(TOKEN_BOT)
        self.__chat_id = CHAT_ID


    def life_cycle(self) -> None:
        try:
            while True:
                time.sleep(60)
                current_data = datetime.now() # актуальная дата и время
                if current_data.hour == 16 and current_data.minute == 15:
                    self.__bot.send_message(self.__chat_id, sheets.main())
                if current_data.hour == 16 and current_data.minute == 20:
                    self.__bot.send_message(self.__chat_id, sheets_two.main())
        except Exception as exc:
            print(
                exc
            )

if __name__ == '__main__':
    print('go script!!!')
    bot = Bot()
    bot.life_cycle()
else:
    print('xxxxxxxxxxxxx')


    #####