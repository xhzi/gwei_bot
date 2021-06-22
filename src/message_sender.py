from tg.notice_sender import send_message
from db.crud import session
from db.db_connect import User
from tg.notice_sender import send_message
import telegram

if __name__ == '__main__':
    users = session.query(User).all()
    text = """
⚠️⚠️⚠️ Need your support ⚠️⚠️⚠️
https://gitcoin.co/grants/2137/eth-gas-price-telegram-bot
Please support the project. This is necessary to maintain and develop the service. Any participation, even 1 DAI, is important."""
    sended = 0
    deleted = 0
    for user in users:
        try:
            send_message(user.tg_id, text)
            sended += 1
        except telegram.error.Unauthorized:
            session.delete(user)
            session.commit()
            deleted += 1
        print(f'sended: {sended}, deleted: {deleted}, last: {user.id}')