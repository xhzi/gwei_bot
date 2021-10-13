from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram.error import BadRequest
import tg.texts as texts
from tg.bot import bot
from tg.controller import Controller
from tg.keyboards import main_menu_keyboard, create_notice_keyboard
import logging


UPDATED_NOTICES_LIST = 0
ENTER_GAS_PRICE, CREATE_NOTICE = 0, 1


def start(update, context):
    text = texts.start
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=main_menu_keyboard)


def help(update, context):
    text = texts.help
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def info(update, context):
    text = texts.info
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')


def gas_price(update, context):
    text = controller.get_gas_price(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown', reply_markup=main_menu_keyboard)


# def fastest(update, context):
#     text = controller.create_notice_by_command(update, 'fastest')
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def fast(update, context):
    text = controller.create_notice_by_command(update, 'fast')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def average(update, context):
    text = controller.create_notice_by_command(update, 'average')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def slow(update, context):
    text = controller.create_notice_by_command(update, 'slow')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get_notices(update, context):
    text, keyboard = controller.get_notices(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=keyboard)
    return UPDATED_NOTICES_LIST


def update_notices_list(update, context):
    text, keyboard = controller.update_notices_list(update)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return UPDATED_NOTICES_LIST


def create_notice_command(update, context):
    text, keyboard = 'Choice tx speed:', create_notice_keyboard
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=keyboard)
    return ENTER_GAS_PRICE


def enter_gas_price(update, context):
    text = 'Enter expected gas price:'
    update.callback_query.edit_message_text(text=text)
    context.user_data['gp_type'] = update.callback_query.data
    context.user_data['callback_query'] = update.callback_query
    return CREATE_NOTICE


def create_notice(update, context):
    callback_query = context.user_data['callback_query']
    is_created, text = controller.create_notice_by_keyboard(update, context.user_data['gp_type'])
    if is_created:
        callback_query.edit_message_text(text=text)
        return ConversationHandler.END
    else:
        try:
            callback_query.edit_message_text(text=text)
        except BadRequest:
            pass
        return CREATE_NOTICE


def create_conversation_handlers():
    # it should be inside a function
    create_notice_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('create_notice', create_notice_command)],
        states={
            ENTER_GAS_PRICE: [CallbackQueryHandler(enter_gas_price, pattern=r'(fast|average|slow)')],
            CREATE_NOTICE: [MessageHandler(Filters.regex(r"(\d+\.\d+|\d+)"), create_notice)]
        },
        allow_reentry=True,
        fallbacks=[],

    )

    get_notices_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('get_notices', get_notices)],
        states={
            UPDATED_NOTICES_LIST: [CallbackQueryHandler(update_notices_list, pattern=r'^[0-9]+$')]
        },
        allow_reentry=True,
        fallbacks=[],

    )

    return create_notice_conversation_handler, get_notices_conversation_handler


def create_handlers():
    create_notice_conversation_handler, get_notices_conversation_handler = create_conversation_handlers()

    handlers = [CommandHandler('start', start), CommandHandler('help', help), CommandHandler('info', info),
                CommandHandler('gas_price', gas_price),
                CommandHandler('fast', fast), CommandHandler('average', average), CommandHandler('slow', slow),
                create_notice_conversation_handler, get_notices_conversation_handler, ]

    return handlers


def interface(gp_data, eth_price):

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO, filename="interface_log.log")

    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher

    global controller
    controller = Controller(gp_data, eth_price)

    handlers = create_handlers()

    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()
