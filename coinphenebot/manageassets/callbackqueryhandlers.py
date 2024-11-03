from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, ForceReply
from telebot.util import quick_markup
from manageassets import replies, queries, manageassetservice
import tokeninfo
import tokeninfo.tokeninfoservice
from db import SplToken
import common
import wallet as walletmodule
import config

# async def callback_buy_with_x_sol(bot: AsyncTeleBot, query: CallbackQuery):
#     manageassetservice.update_managed_asset_type("buy_with_x_sol", query.from_user.id)
#     await bot.send_message(query.message.chat.id, replies.ENTER_ASSET_TO_BUY_WITH_X_SOL, reply_markup=ForceReply())


async def callback_manage_assets(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        chat_id = query.message.chat.id
        await bot.send_chat_action(chat_id, action="typing")
        user_wallet = walletmodule.get_wallet_by_telegram_id(query.from_user.id)
        """
        data = get_tokens_in_wallet(user_wallet.public_key)
        if data is None:
            return await bot.send_message(chat_id, common.SOMETHING_WENT_WRONG)

        if len(data["tokens"]) == 0:
            return await bot.send_message(chat_id, "You do not have any open positions", reply_markup=quick_markup({
                'Close': { 'callback_data': queries.Q_GO_BACK }
            }, row_width=1))
        elif len(data["tokens"]) == 1:
            if data["tokens"][0]["symbol"] == "SOL":
                sol_balance = data["tokens"][0]["accounts"][0]["uiAmount"]
                if sol_balance == 0:
                    return await bot.send_message(chat_id, "You do not have any open positions", reply_markup=quick_markup({
                        'Close': { 'callback_data': queries.Q_GO_BACK }
                    }, row_width=1))
                
                return await bot.send_message(chat_id, f"Balances:\n\nSOL: {sol_balance}\n\nYou do not have any tokens but you have a SOL balance. Click the button below to manage your SOL asset", reply_markup=quick_markup({
                        'Manage SOL Asset': {'callback_data': queries.Q_MANAGE_SOL_ASSET},
                    }, row_width=1))

        user_balances = []
        for token in data["tokens"]:
            current_balance = {
                "name": token["name"],
                "symbol": token["symbol"],
                "amount": token["totalUiAmount"],
                "address": token["mint"]
            }
            if "price" in token:
                current_balance["pnl_usd"] = token["price"]["usdChange"]
                current_balance["pnl_sol"] = token["price"]["change"]
                current_balance["value_usd"] = token["price"]["usdPrice"]
                current_balance["value_sol"] = token["price"]["price"]
                if "mc" in token["price"]:
                    current_balance["market_cap"] = token["price"]["mc"]
            user_balances.append(current_balance)

            # save the token to the cache (currently the db) if it hasn't been saved
            create_spl_token(SplToken(symbol=token["symbol"], name=token["name"], address=token["mint"]))

        total_usd = data["value"]["total"]
        # total_pnl_usd = data["value"]["change"]
        total_change_usd = data["value"]["percentage"]

        total_sol = data["solValue"]["total"]
        # total_pnl_sol = data["solValue"]["change"]
        total_change_sol = data["solValue"]["percentage"]

        response = "Token balances:\n\n"
        for bal in user_balances:
            name = bal["name"]
            symbol = bal["symbol"]
            amount = bal["amount"]
            address = bal["address"]
            pnl_sol = bal["pnl_sol"] if "pnl_sol" in bal else "0"
            pnl_usd = bal["pnl_usd"] if "pnl_usd" in bal else "0"
            value_sol = bal["value_sol"] if "value_sol" in bal else "0"
            value_usd = bal["value_usd"] if "value_sol" in bal else "0"
            mc = bal["market_cap"] if "market_cap" in bal else "No market cap"
            response += (f"\n*{name}*:\n\n*Balance*: {amount} {symbol}\n*Address*: {address}\n*PnL SOL*: {pnl_sol}\n*PnL USD*: {pnl_usd}"
                         f"\n*Value(SOL)*: {value_sol}\n*Value(USD)*: {value_usd}\n*Market Cap*: {mc}\n")
        response += (f"\n\n*SUMMARY*\n\n*Total balance(SOL)*: {total_sol}\n*Total balance(usd)*: {total_usd}\n*Total PnL(SOL)*: {total_change_sol}%\n"
                     f"*Total PnL(USD)*: {total_change_usd}%")
        response += "\n\n👇"
        """
        # """
        data = walletmodule.get_wallet_balance("DJ497RGbwHwjFqr3tyGkhQSmcjpGFrVa6B2WfFQQXunp")
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
        # """
        
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
    await bot.send_message(query.message.chat.id, replies.ENTER_ASSET_TO_SELL_100_PERCENT, reply_markup=ForceReply())


async def callback_sell_x_percent(bot: AsyncTeleBot, query: CallbackQuery):
    manageassetservice.update_managed_asset_type("sell_x_percent", query.from_user.id)
    walletmodule.update_pending_txn_input_mint(config.native_mint, query.from_user.id)
    await bot.send_message(query.message.chat.id, replies.ENTER_ASSET_TO_SELL_X_PERCENT, reply_markup=ForceReply())


async def callback_refresh(bot: AsyncTeleBot, query: CallbackQuery):
    await callback_manage_assets(bot, query)


async def callback_view_token_chart(bot: AsyncTeleBot, query: CallbackQuery):
    pass
