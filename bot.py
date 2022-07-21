from aiogram.utils import executor
from tools.bot_tools import dp, on_startup
from handlers.commands import command_handlers
from handlers.callbacks import callback_handlers
from handlers.messages import message_handlers

command_handlers(dp)
callback_handlers(dp)
message_handlers(dp)

if __name__ =='__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
