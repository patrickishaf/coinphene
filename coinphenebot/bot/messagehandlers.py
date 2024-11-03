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


async def handle_assets(bot: AsyncTeleBot, message: Message):
    await bot.send_message(message.chat.id, 'here are your assets')


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
        # balances = walletmodule.get_tokens_in_wallet(wallet.public_key)
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
    await bot.send_message(message.chat.id, 'this is your wallet and this is your wallet balance')
