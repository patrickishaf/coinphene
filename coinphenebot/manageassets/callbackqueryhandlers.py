from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, ForceReply
from telebot.util import quick_markup
from manageassets import replies, queries, manageassetservice
import tokeninfo
import tokeninfo.tokeninfoservice
import common
import wallet as walletmodule
import config


async def callback_manage_assets(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        chat_id = query.message.chat.id
        await bot.send_chat_action(chat_id, action="typing")
        user_wallet = walletmodule.get_wallet_by_telegram_id(query.from_user.id)
        data = walletmodule.get_wallet_balance(user_wallet.public_key)
        sol_balance = data["native_balance"]["balance"]
        # if the user has no balances
        if sol_balance == 0 and len(data["token_balances"]) == 0:
            return await bot.send_message(chat_id, "You do not have any open positions", reply_markup=quick_markup({
                    'Close': { 'callback_data': queries.Q_GO_BACK }
                }, row_width=1))
        elif len(data["token_balances"]) == 0:
            return await bot.send_message(chat_id, f"Balances:\n\nSOL: {sol_balance}\n\nYou do not have any tokens but you have a SOL balance. Click the button below to manage your SOL asset", reply_markup=quick_markup({
                    'Manage SOL Asset': {'callback_data': queries.Q_MANAGE_SOL_ASSET},
                }, row_width=1))
        
        mints = [item["mint"] for item in data["token_balances"]]
        #  TODO: If the mints are more than 30, split the array of mints into batches of 30. reason is that geckoterminal supports a maximum of 30 per request
        multi_token_info = tokeninfo.get_multi_token_info(",".join(mints))

        response = "Token balances:\n\n"
        current_index = 0
        for info in multi_token_info["data"]:
            name = info["attributes"]["name"]
            symbol = info["attributes"]["symbol"]
            amount = data["token_balances"][current_index]["balance"]
            address = info["attributes"]["address"]
            price_usd = eval(info["attributes"]["price_usd"])
            value_sol = price_usd * amount
            mc = info["attributes"]["market_cap_usd"]
            mc = 0 if mc is None else eval(mc)
            response += (f"\n*{name}*:\n\n*Balance*: {format(amount, '.10f')} {symbol}\n*Address*: `{address}`"
                         f"\n*Value(SOL)*: {format(value_sol, '.10f')}\n*Market Cap*: {format(mc, '.2f')}\n")
            current_index += 1
        response += "\n\n👇"
        
        manageassetservice.create_managed_asset(query.from_user.id)
        await bot.send_message(chat_id, response, reply_markup=quick_markup({
            'Buy with x SOL': { 'callback_data': queries.Q_MA_BUY_WITH_X_SOL },
            'Sell 100%': { 'callback_data': queries.Q_SELL_100_PERCENT },
            'Sell x%': { 'callback_data': queries.Q_SELL_X_PERCENT },
            'Refresh': { 'callback_data': queries.Q_REFRESH },
            'View Token Chart': { 'callback_data': queries.Q_VIEW_TOKEN_CHART },
        }, row_width=2))
        # await bot.send_message(chat_id, replies.ENTER_ASSET_SYMBOL_TO_MANAGE, reply_markup=ForceReply())
    except Exception as e:
        print(f"failed to process manage assets callback. error: {e}")
        await bot.send_message(chat_id, common.SOMETHING_WENT_WRONG)


async def callback_buy_with_x_sol(bot: AsyncTeleBot, query: CallbackQuery):
    walletmodule.update_pending_txn_output_mint(config.native_mint, query.from_user.id)
    await bot.send_message(query.message.chat.id, replies.ENTER_ASSET_TO_BUY_WITH_X_SOL, reply_markup=ForceReply())


async def callback_sell_100_percent(bot: AsyncTeleBot, query: CallbackQuery):
    manageassetservice.update_managed_asset_type("sell_100_percent", query.from_user.id)
    walletmodule.update_pending_txn_type("sell_100_percent", query.from_user.id)
    await bot.send_message(query.message.chat.id, replies.ENTER_ASSET_TO_SELL_100_PERCENT, reply_markup=ForceReply())


async def callback_sell_x_percent(bot: AsyncTeleBot, query: CallbackQuery):
    manageassetservice.update_managed_asset_type("sell_x_percent", query.from_user.id)
    walletmodule.update_pending_txn_input_mint(config.native_mint, query.from_user.id)
    await bot.send_message(query.message.chat.id, replies.ENTER_ASSET_TO_SELL_X_PERCENT, reply_markup=ForceReply())


async def callback_refresh(bot: AsyncTeleBot, query: CallbackQuery):
    await callback_manage_assets(bot, query)


async def callback_view_token_chart(bot: AsyncTeleBot, query: CallbackQuery):
    pass
