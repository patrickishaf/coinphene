from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
from telebot.util import quick_markup
import settings.queries as queries
import common.queries as commonqueries

async def callback_settings(bot: AsyncTeleBot, query: CallbackQuery):
    await bot.send_message(query.message.chat.id, "What would you like to do?", reply_markup=quick_markup({
        "📌 Pin Bot": {"callback_data": queries.Q_PIN_BOT},
        "📝 Language": {"callback_data": queries.Q_CHANGE_LANGUAGE},
        "❌ Cancel": {"callback_data": commonqueries.Q_GO_BACK}
    }, row_width=2))
