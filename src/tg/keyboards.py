from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


def create_user_notices_keyboard(notices):
    notices.sort(key=lambda i: i.gp)
    keyboard = []
    for notice in notices:
        button = [InlineKeyboardButton(f'{notice.type.name} {notice.gp} - delete', callback_data=notice.id)]
        keyboard.append(button)
    return InlineKeyboardMarkup(keyboard)


create_notice_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton('fastest', callback_data='fastest'), InlineKeyboardButton('fast', callback_data='fast')],
     [InlineKeyboardButton('standard', callback_data='standard'), InlineKeyboardButton('slow', callback_data='slow')]])

main_menu_keyboard = ReplyKeyboardMarkup([[KeyboardButton('/gas_price')],
                                          [KeyboardButton('/create_notice'), KeyboardButton('/get_notices')]],
                                         resize_keyboard=True)
