from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, ForceReply
from telebot.util import quick_markup
import bot.replies as replies
from wallet import walletservice, transactionservice
from db import Wallet
import bot.queries as queries
import manageassets as manageassets
import wallet.queries as walletqueries
from tokeninfo import tokeninfoservice
from db import SplToken


async def callback_buy(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        # update pending transaction type to buy
        transactionservice.update_pending_txn_type('BUY', user_id=query.from_user.id)
        
        chat_id = query.message.chat.id

        # confirm that the user has sol balance
        user_wallet = walletservice.get_wallet_by_telegram_id(query.from_user.id)
        if user_wallet is None:
            new_wallet = walletservice.generate_wallet()
            walletservice.save_wallet_to_user(Wallet(
                public_key=new_wallet["public_key"],
                private_key=new_wallet["secret_key"],
                user_telegram_id=query.from_user.id,
            ))
            user_wallet = new_wallet
        
        await bot.send_message(chat_id, replies.BUY_RESPONSE)
        await bot.send_message(chat_id, replies.ENTER_TOKEN_ADDRESS_OR_PUMP_FUN_LINK_TO_BUY, reply_markup=ForceReply(input_field_placeholder="4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R"))
    except Exception as e:
        print(f"failed to process buy callback. error: {e}")
        await bot.send_message(chat_id, replies.SOMETHING_WENT_WRONG)


async def callback_buy_with_x_sol(bot: AsyncTeleBot, query: CallbackQuery):
    await bot.send_message(query.message.chat.id, replies.ENTER_AMOUNT_OF_SOL_TO_SPEND, reply_markup=ForceReply(input_field_placeholder="0.01234"))


async def callback_create_wallet(bot: AsyncTeleBot, query: CallbackQuery):
    chat_id = query.message.chat.id
    try:
        user_wallet = walletservice.get_wallet_by_telegram_id(query.from_user.id)
        if user_wallet is not None:
            return await bot.send_message(chat_id, "you already have a wallet. To reset your wallet, go to settings", reply_markup=quick_markup({
                'Settings': { 'callback_data': queries.Q_SETTINGS }
            }, row_width=1))
        
        new_wallet = walletservice.generate_wallet()
        walletservice.save_wallet_to_user(Wallet(
            public_key=new_wallet["public_key"],
            private_key=new_wallet["secret_key"],
            user_telegram_id=query.from_user.id
        ))
        await bot.send_message(chat_id, "a brand new wallet has been generated for you\! your wallet address is👇")
        await bot.send_message(chat_id, new_wallet["public_key"])
    except Exception as e:
        await bot.send_message(chat_id, "I can not create a wallet for you at this time. Please try again later")


async def callback_go_back(bot: AsyncTeleBot, query: CallbackQuery):
    await bot.delete_message(query.message.chat.id, query.message.id)


async def callback_help(bot: AsyncTeleBot, query: CallbackQuery):
    chat_id = query.message.chat.id

    await bot.send_message(chat_id, "help is currently under construction")


async def callback_sell(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        chat_id = query.message.chat.id
        # 1. Ensure user has balances
        user_telegram_id = query.from_user.id
        existing_wallet = walletservice.get_wallet_by_telegram_id(user_telegram_id)
        if existing_wallet is None:
            return await bot.send_message(chat_id, "you don't have a wallet yet. Tap the button below to create one", reply_markup=quick_markup({
                'Create Wallet': {'callback_data': walletqueries.Q_CREATE_WALLET},
            }, row_width=1))

        else:
            transactionservice.update_pending_txn_type('SELL', user_id=query.from_user.id)
            data = walletservice.get_wallet_balance(existing_wallet.public_key, detailed=True)
            if len(data["token_balances"]) == 0:
                return await bot.send_message(chat_id, "you do not have enough token balances to sell")
            addresses = [item["mint"] for item in data["token_balances"]]
            multi_token_info = tokeninfoservice.get_multi_token_info(",".join(addresses))

            response = "Token balances:\n"
            current_index = 0
            for info in multi_token_info["data"]:
                name = info["attributes"]["name"]
                symbol = info["attributes"]["symbol"]
                amount = data["token_balances"][current_index]["balance"]
                address = info["attributes"]["address"]
                response += f"\n*{name}*: {amount:.10f} {symbol}\n*Address*: `{address}`\n(👆tap to copy)\n\n"

                # cache the spl token for faster lookup in case of next time
                cached_token = SplToken(
                    address=address,
                    name=name,
                    symbol=symbol
                )
                tokeninfoservice.create_spl_token(cached_token)
                current_index += 1
            response += "👇"
            
            await bot.send_message(chat_id, response)
            await bot.send_message(chat_id, replies.ENTER_TOKEN_ADDRESS_TO_SELL, reply_markup=ForceReply(input_field_placeholder="e.g ABC"))
    except Exception as e:
        print(f"failed to process sell callback. error: {e}")
        await bot.send_message(chat_id, replies.SOMETHING_WENT_WRONG)
