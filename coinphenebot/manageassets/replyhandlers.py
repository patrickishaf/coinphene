from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, ForceReply
from manageassets import manageassetservice, replies
from wallet import walletservice
import common.replies as commonreplies
import config


async def enter_amount_of_token(bot: AsyncTeleBot, reply: Message):
    chat_id = reply.chat.id
    try:
        amount = eval(reply.text)
        manageassetservice.update_managed_asset_amount(amount)
        managed_asset = manageassetservice.get_managed_asset_by_uid(reply.from_user.id)
        txn = walletservice.buy_token(amount, managed_asset.ticker)
        if txn is None:
            return await bot.send_message(chat_id, commonreplies.TRANSACTION_FAILED)
        return await bot.send_message(chat_id, commonreplies.TRANSACTION_SENT)
    except Exception as e:
        print(f"failed to resolve enter amount of sol. error: {e}")
        await bot.send_message(chat_id, "something went wrong. please try again")
        await bot.send_message(chat_id, replies.ENTER_AMOUNT_OF_SOL)


async def enter_asset_to_buy_with_x_sol(bot: AsyncTeleBot, reply: Message):
    chat_id = reply.chat.id
    try:
        manageassetservice.update_managed_asset_ticker(reply.text, reply.from_user.id)
        await bot.send_message(chat_id, replies.ENTER_AMOUNT_OF_SOL, reply_markup=ForceReply())
    except Exception as e:
        print(f"failed to resolve enter asset to buy with x sol. error: {e}")
        await bot.send_message(chat_id, "something went wrong. please try again")
        await bot.send_message(chat_id, replies.ENTER_ASSET_TO_BUY_WITH_X_SOL)


async def enter_asset_to_sell_100_percent(bot: AsyncTeleBot, reply: Message):
    chat_id = reply.chat.id
    try:
        print("handling enter asset to sell 100%")

        if reply.text.upper() == "SOL":
            return await bot.send_message(chat_id, "You can not sell your SOL. If you want to withdraw your SOL you can send it to another address")

        manageassetservice.update_managed_asset_ticker(reply.text, reply.from_user.id)
        wallet = walletservice.get_wallet_by_telegram_id(reply.from_user.id)
        balances = walletservice.get_tokens_in_wallet(wallet.public_key)
        matching_balance = None
        matching_ticker = None
        matching_token_address = None
        for token in balances["tokens"]:
            if token["symbol"] == reply.text.upper():
                matching_balance = token["accounts"][0]["uiAmount"]
                matching_ticker = token["symbol"]
                matching_token_address = token["mint"]
                break
        if matching_balance is None or matching_ticker is None or matching_token_address is None:
            await bot.send_message(chat_id, replies.TOKEN_UNAVAILABLE)
            return await bot.send_message(chat_id, replies.ENTER_ASSET_TO_SELL_100_PERCENT, reply_markup=ForceReply())
        
        charges_percent = eval(config.txn_charge)
        charges = (charges_percent / 100) * matching_balance

        charges_deduction_txn = walletservice.sell_token(charges, matching_token_address)
        if charges_deduction_txn is None:
            return await bot.send_message(chat_id, commonreplies.TRANSACTION_FAILED)

        token_sale_txn = walletservice.sell_token(matching_balance - charges, matching_token_address)
        if token_sale_txn is None:
            return await bot.send_message(chat_id, commonreplies.TRANSACTION_FAILED)
        
        await bot.send_message(chat_id, commonreplies.TRANSACTION_SENT)
    except Exception as e:
        print(f"failed to resolve enter asset to sell 100%. error: {e}")
        await bot.send_message(chat_id, "something went wrong. please try again")
        await bot.send_message(chat_id, replies.ENTER_ASSET_TO_SELL_100_PERCENT)


async def enter_asset_to_sell_x_percent(bot: AsyncTeleBot, reply: Message):
    chat_id = reply.chat.id
    try:
        print("handling enter asset to sell x%")

        if reply.text.upper() == "SOL":
            return await bot.send_message(chat_id, "You can not sell your SOL. If you want to withdraw your SOL you can send it to another address")

        manageassetservice.update_managed_asset_ticker(reply.text, reply.from_user.id)
        await bot.send_message(chat_id, replies.ENTER_PERCENTAGE_OF_TOKEN_TO_SELL, reply_markup=ForceReply(input_field_placeholder="50"))
    except Exception as e:
        print(f"failed to resolve enter asset to sell 100%. error: {e}")
        await bot.send_message(chat_id, "something went wrong. please try again")
        await bot.send_message(chat_id, replies.ENTER_ASSET_TO_SELL_100_PERCENT)


async def enter_percentage_of_token_to_sell(bot: AsyncTeleBot, reply: Message):
    chat_id = reply.chat.id
    try:
        percentage = eval(reply.text)
        manageassetservice.update_managed_asset_amount(percentage)
        managed_asset = manageassetservice.get_managed_asset_by_uid(reply.from_user.id)
        ticker = managed_asset.ticker

        wallet = walletservice.get_wallet_by_telegram_id(reply.from_user.id)
        balances = walletservice.get_tokens_in_wallet(wallet.public_key)
        matching_balance = None
        matching_ticker = None
        matching_token_address = None
        for token in balances["tokens"]:
            if token["symbol"] == ticker.upper():
                matching_balance = eval(token["accounts"][0]["uiAmount"]) * (percentage / 100)
                matching_ticker = token["symbol"]
                matching_token_address = token["mint"]
                break
        if matching_balance is None or matching_ticker is None or matching_token_address is None:
            await bot.send_message(chat_id, replies.TOKEN_UNAVAILABLE)
            return await bot.send_message(chat_id, replies.ENTER_ASSET_TO_SELL_100_PERCENT, reply_markup=ForceReply())
        
        charges_percent = eval(config.txn_charge)
        charges = (charges_percent / 100) * matching_balance

        charges_deduction_txn = walletservice.sell_token(charges, matching_token_address)
        if charges_deduction_txn is None:
            return await bot.send_message(chat_id, commonreplies.TRANSACTION_FAILED)

        token_sale_txn = walletservice.sell_token(matching_balance - charges, matching_token_address)
        if token_sale_txn is None:
            return await bot.send_message(chat_id, commonreplies.TRANSACTION_FAILED)
    except Exception as e:
        print(f"failed to resolve enter percentage of asset to sell. error: {e}")
        await bot.send_message(chat_id, "something went wrong. please try again")
        await bot.send_message(chat_id, replies.ENTER_PERCENTAGE_OF_TOKEN_TO_SELL, reply_markup=ForceReply(input_field_placeholder="50"))
