from telebot.async_telebot import AsyncTeleBot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery
from config import bot_token
from bot import commands, queries, messagehandlers, callbackqueryhandlers, replyhandlers, middlewares, replyrouter
import manageassets
import wallet
import referral
import settings
import logfire


bot = AsyncTeleBot(bot_token, parse_mode="Markdown")
logfire.configure()


@bot.message_handler(commands=[commands.c_assets])
async def handle_assets(message: Message):
    await messagehandlers.handle_assets(bot, message)


@bot.message_handler(commands=[commands.c_start])
async def handle_start(message: Message):
    await messagehandlers.handle_start(bot, message)


@bot.message_handler(commands=[commands.c_settings])
async def handle_settings(message: Message):
    await messagehandlers.handle_settings(bot, message)


@bot.message_handler(commands=[commands.c_help])
async def handle_settings(message: Message):
    await messagehandlers.handle_help_command(bot, message)


@bot.message_handler(commands=[commands.c_wallet])
async def handle_wallet(message: Message):
    await messagehandlers.handle_wallet(bot, message)


@bot.message_handler()
async def handle_reply(message: Message):
    if message.reply_to_message is not None:
        await replyrouter.route_reply_to_handler(bot, message)
    else:
        print(f"unrecognized message: {message}")
        await replyhandlers.handle_enter_token_address_or_pump_fun_link_to_buy(bot, message)


@bot.callback_query_handler(func=lambda x: x.json["data"] == queries.Q_BUY)
async def handle_buy(query: CallbackQuery):
    await callbackqueryhandlers.callback_buy(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == queries.Q_CREATE_WALLET)
async def handle_create_wallet(query: CallbackQuery):
    await callbackqueryhandlers.callback_create_wallet(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == queries.Q_GO_BACK)
async def handle_go_back(query: CallbackQuery):
    await callbackqueryhandlers.callback_go_back(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == queries.Q_HELP)
async def handle_help(query: CallbackQuery):
    await callbackqueryhandlers.callback_help(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == queries.Q_SELL)
async def handle_sell(query: CallbackQuery):
    await callbackqueryhandlers.callback_sell(bot, query)


@bot.callback_query_handler(func=lambda x:x.json["data"] == manageassets.Q_MA_BUY_WITH_X_SOL)
async def handle_ma_buy_with_x_sol(query: CallbackQuery):
    await manageassets.callback_buy_with_x_sol(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == manageassets.Q_MANAGE_ASSETS)
async def handle_manage_assets(query: CallbackQuery):
    await manageassets.callback_manage_assets(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == manageassets.Q_SELL_100_PERCENT)
async def handle_sell_100_percent(query: CallbackQuery):
    await manageassets.callback_sell_100_percent(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == manageassets.Q_SELL_X_PERCENT)
async def handle_sell_x_percent(query: CallbackQuery):
    await manageassets.callback_sell_x_percent(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == manageassets.Q_REFRESH)
async def handle_refresh(query: CallbackQuery):
    await manageassets.callback_refresh(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == manageassets.Q_VIEW_TOKEN_CHART)
async def handle_view_token_chart(query: CallbackQuery):
    await manageassets.callback_view_token_chart(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == referral.Q_REFERRAL)
async def handle_view_token_chart(query: CallbackQuery):
    await referral.callback_refer(bot, query)


@bot.callback_query_handler(func = lambda x: x.json["data"] == settings.Q_SETTINGS)
async def handle_settings(query: CallbackQuery):
    await settings.callback_settings(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == wallet.Q_BUY_WITH_1_SOL)
async def handle_buy_with_1_sol(query: CallbackQuery):
    await wallet.callback_buy_with_1_sol(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == wallet.Q_BUY_WITH_2_SOL)
async def handle_buy_with_2_sol(query: CallbackQuery):
    await wallet.callback_buy_with_2_sol(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == wallet.Q_BUY_WITH_X_SOL)
async def handle_buy_with_x_sol(query: CallbackQuery):
    await wallet.callback_buy_with_x_sol(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == wallet.Q_CONFIRM_EXPORT_PRIVATE_KEY)
async def handle_confirm_export_private_key(query: CallbackQuery):
    await wallet.callback_confirm_export_pk(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == wallet.Q_DEPOSIT_SOL)
async def handle_deposit_sol(query: CallbackQuery):
    await wallet.callback_deposit_sol(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == wallet.Q_EXPORT_PRIVATE_KEY)
async def handle_export_private_key(query: CallbackQuery):
    await wallet.callback_export_private_key(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == wallet.Q_REFRESH_BUY)
async def handle_refresh_buy(query: CallbackQuery):
    await wallet.callback_refresh_buy(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == wallet.Q_WALLET)
async def handle_wallet(query: CallbackQuery):
    await wallet.callback_wallet(bot, query)


@bot.callback_query_handler(func=lambda x: x.json["data"] == wallet.Q_WITHDRAW_X_SOL)
async def handle_withdraw_x_sol(query: CallbackQuery):
    await wallet.callback_withdraw_x_sol(bot, query)
