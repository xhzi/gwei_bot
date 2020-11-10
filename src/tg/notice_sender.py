from config import OLD_GP, TIMEOUT
from db.crud import get_notices_larger_arg_by_type, delete_notice, delete_user
from tg.bot import bot
import logging
import time
from telegram.error import Unauthorized


def send_message(tg_id, text):
    result = bot.send_message(chat_id=tg_id, text=text)
    return result


def check_ready_notices(gp_now):
    ready_notices = []
    for key in gp_now.keys():
        for notice in get_notices_larger_arg_by_type(gp_now[key], key):
            ready_notices.append(notice)

    return ready_notices


def is_1_less_2(gp1, gp2):
    for key in gp1.keys():
        if gp1[key] < gp2[key]:
            return True


def notice_sender(gp_data):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO, filename="notice_sender_log.log")

    gp_old = OLD_GP
    gp_now = gp_data.copy()
    while True:
        if is_1_less_2(gp_now, gp_old):
            ready_notices = check_ready_notices(gp_now)
            for notice in ready_notices:
                try:
                    notice_id, gp, tg_id, gp_type = notice.id, notice.gp, notice.user.tg_id, notice.type
                    text = f'{gp_type.name} {gp} completed. Current {gp_type.name}: {gp_now[gp_type.name]}'
                    res = send_message(tg_id, text)
                    if res:
                        delete_notice(notice_id)
                except Unauthorized:
                    # if user unsubscribed from bot
                    delete_user(notice.user)
                except:
                    pass
        gp_old = gp_now.copy()
        time.sleep(TIMEOUT)
        gp_now = gp_data.copy()
