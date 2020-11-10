from telegram.bot import Bot
from telegram.utils.request import Request
from config import TOKEN

request = Request(con_pool_size=10)
bot = Bot(TOKEN, request=request)
