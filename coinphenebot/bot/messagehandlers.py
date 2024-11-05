from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot.util import quick_markup
from bot import replies, queries
import wallet as walletmodule
from db import Wallet
import manageassets
import referral as referral
from settings import userservice
import common
from manageassets import manageassetservice
import tokeninfo
import config


async def handle_assets(bot: AsyncTeleBot, message: Message):
    try:
        chat_id = message.chat.id
        await bot.send_chat_action(chat_id, action="typing")
        user_wallet = walletmodule.get_wallet_by_telegram_id(message.from_user.id)
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
        
        manageassetservice.create_managed_asset(message.from_user.id)
        await bot.send_message(chat_id, response, reply_markup=quick_markup({
            'Buy with x SOL': { 'callback_data': manageassets.Q_MA_BUY_WITH_X_SOL },
            'Sell 100%': { 'callback_data': manageassets.Q_SELL_100_PERCENT },
            'Sell x%': { 'callback_data': manageassets.Q_SELL_X_PERCENT },
            'Refresh': { 'callback_data': manageassets.Q_REFRESH },
            'View Token Chart': { 'callback_data': manageassets.Q_VIEW_TOKEN_CHART },
        }, row_width=2))
        # await bot.send_message(chat_id, replies.ENTER_ASSET_SYMBOL_TO_MANAGE, reply_markup=ForceReply())
    except Exception as e:
        print(f"failed to process manage assets callback. error: {e}")
        await bot.send_message(chat_id, common.SOMETHING_WENT_WRONG)


async def handle_start(bot: AsyncTeleBot, message: Message):
    """
    Items to get for user:
    1. public key for wallet
    2. private key for wallet
    3. SOL balance
    """
    await bot.send_chat_action(message.chat.id, "typing")

    # handle referral-related functions
    existing_user = userservice.get_user_by_tg_id(message.from_user.id)
    if existing_user is None:
        userservice.save_user(message.from_user.id, message.from_user.username, message.chat.id)
        referral.create_referral_link_for_user(message.from_user.id)
    elif existing_user.referral_code is None:
        referral.create_referral_link_for_user(message.from_user.id)
    
    wallet: Wallet = walletmodule.get_wallet_by_telegram_id(message.from_user.id)
    if wallet is None:
        print('user does not have a wallet')
        
        new_wallet = walletmodule.generate_wallet()
        walletmodule.save_wallet_to_user(Wallet(
            public_key=new_wallet["public_key"],
            private_key=new_wallet["secret_key"],
            user_telegram_id=message.from_user.id
        ))
        walletmodule.create_pending_txn(user_id=message.from_user.id)
        reply = replies.get_welcome_message(new_wallet["public_key"])
        await bot.send_message(message.chat.id, text=reply, reply_markup=quick_markup({
            '💸 Buy': {'callback_data': queries.Q_BUY},
            '💵 Sell': {'callback_data': queries.Q_SELL},
            '💰 My Assets': {'callback_data': manageassets.Q_MANAGE_ASSETS},
            '💳 Wallet': {'callback_data': walletmodule.Q_WALLET},
            # '⚙️ Settings': {'callback_data': queries.Q_SETTINGS},
            '❓ Help': {'callback_data': queries.Q_HELP},
            '🙋‍♂️ Referral': {'callback_data': referral.Q_REFERRAL},
            '❌ Back': {'callback_data': queries.Q_GO_BACK}
        }, row_width=2))
    else:
        data = walletmodule.get_sol_balance(wallet.public_key)
        sol_balance = data["balance"]
        reply = replies.get_return_message(wallet.public_key, sol_balance)
        await bot.send_message(message.chat.id, text=reply, reply_markup=quick_markup({
            '💸 Buy': {'callback_data': queries.Q_BUY},
            '💵 Sell': {'callback_data': queries.Q_SELL},
            '💰 My Assets': {'callback_data': manageassets.Q_MANAGE_ASSETS},
            '💳 Wallet': {'callback_data': walletmodule.Q_WALLET},
            # '⚙️ Settings': {'callback_data': queries.Q_SETTINGS},
            '❓ Help': {'callback_data': queries.Q_HELP},
            '🙋‍♂️ Referral': {'callback_data': referral.Q_REFERRAL},
            '❌ Back': {'callback_data': queries.Q_GO_BACK}
        }, row_width=2))
    # Check for referral links
    if "ref_" in message.text:
        await referral.handle_referral(message.text, message.from_user.id)


async def handle_settings(bot: AsyncTeleBot, message: Message):
    await bot.send_message(message.chat.id, 'here are your settings')


async def handle_help_command(bot: AsyncTeleBot, message: Message):
    await bot.send_message(message.chat.id, 'sure, we can help you with anything')


async def handle_wallet(bot: AsyncTeleBot, message: Message):
    try:
        chat_id = message.chat.id
        await bot.send_chat_action(chat_id, 'typing')
        """
        Things to show user:
        1. Wallet address
        2. Balance in SOL
        3. Balance in USD

        Buttons to show user:
        1. Withdraw x SOL
        2. Deposit SOL
        3. Reset Wallet
        4. Export Private Key
        5. Close
        6. Refresh
        """
        wallet = walletmodule.get_wallet_by_telegram_id(message.from_user.id)
        if wallet is None:
            await bot.send_message(chat_id, "You do not have a wallet yet", reply_markup=quick_markup({
                'Create Wallet': {'callback_data': queries.Q_CREATE_WALLET}
            }, row_width=1))
        
        data = walletmodule.get_sol_balance(wallet.public_key)
        sol_balance = data["balance"]
        
        token_info = tokeninfo.get_token_info(data["mint"])
        usd_balance = eval(token_info["data"]["attributes"]["price_usd"]) * sol_balance
        
        message = f"Wallet\n\n*Address*: `{wallet.public_key}`\n(👆tap to copy)\n\n*Balance (SOL)*: {format(sol_balance, '.6f')} SOL\n*Balance (USD)*: {format(usd_balance, '.2f')} USD"
        await bot.send_message(chat_id, message, reply_markup=quick_markup({
            '⬆️ Withdraw x SOL': {'callback_data': walletmodule.Q_WITHDRAW_X_SOL},
            '⬇️ Deposit SOL': {'callback_data': walletmodule.Q_DEPOSIT_SOL},
            '♻️ Reset Wallet': {'callback_data': walletmodule.Q_RESET_WALLET},
            '🔑 Export Private Key': {'callback_data': walletmodule.Q_EXPORT_PRIVATE_KEY},
            '🔃 Refresh': {'callback_data': walletmodule.Q_WALLET},
            '❌ Close': {'callback_data': common.Q_GO_BACK},
        }))
    except Exception as e:
        print(f"failed to process wallet callback query. error: {e}")
        await bot.send_message(chat_id, common.SOMETHING_WENT_WRONG)
