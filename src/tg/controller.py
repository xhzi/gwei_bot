import tg.texts as texts
from tg import utilities
import db.crud as crud
from tg.keyboards import create_user_notices_keyboard


class Controller:
    def __init__(self, gp_data, eth_price):
        self.gp_data = gp_data
        self.eth_price = eth_price

    def get_gas_price(self):
        gp = self.gp_data
        eth_price = self.eth_price
        text = texts.gp.format(eth_price.data, gp['fastest'], gp['fast'], gp['standard'], gp['slow'])
        return text

    def create_notice(self, tg_id, gp, gp_type):
        if utilities.is_float(gp):
            gp = float(gp)
            gp_now = self.gp_data[gp_type]
            if not crud.is_user_exists(tg_id):
                crud.create_user(tg_id)
            if gp + 4.9 >= gp_now:
                return False, 'Notice gas price close to current price.'
            elif crud.is_user_has_close_notices(tg_id, gp, gp_type):
                return False, 'You have similar notice.'
            else:
                crud.create_notice(tg_id, gp, gp_type)
                return True, 'Success.'
        else:
            return False, f'Error. Use one number to create a notice. Example: "/{gp_type} 13".'

    def create_notice_by_command(self, update, gp_type: str):
        try:
            tg_id, gp = update.effective_chat.id, update.message.text.split(' ')[1]
            is_created, text = self.create_notice(tg_id, gp, gp_type)
            return text
        except:
            return f'Error. Use one number to create a notice. Example: "/{gp_type} 13".'

    def create_notice_by_keyboard(self, update, gp_type: str):
        tg_id, gp = update.effective_chat.id, update.message.text
        is_created, text = self.create_notice(tg_id, gp, gp_type)
        if is_created:
            return is_created, text
        else:
            text += '\nEnter expected gas price:'
            return is_created, text

    def get_notices(self, update):
        tg_id = update.effective_chat.id
        notices = crud.get_user_notices(tg_id)
        keyboard = create_user_notices_keyboard(notices)
        return 'Your notices:', keyboard

    def update_notices_list(self, update):
        tg_id, notice_to_delite = update.effective_chat.id, update.callback_query.data
        crud.delete_notice(notice_to_delite)
        notices = crud.get_user_notices(tg_id)
        keyboard = create_user_notices_keyboard(notices)
        return 'Notice deleted', keyboard
