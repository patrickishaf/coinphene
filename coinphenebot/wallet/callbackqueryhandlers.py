from telebot.async_telebot import AsyncTeleBot
from telebot.util import quick_markup
from telebot.types import CallbackQuery, ForceReply
from wallet import replies, queries, walletservice, transactionservice, pendingwithdrawalservice
import common
from db import Wallet
import base58

async def callback_buy_with_1_sol(bot: AsyncTeleBot, query: CallbackQuery):
    chat_id = query.chat.id
    try:
        amount = 1
        wallet = walletservice.get_wallet_by_telegram_id(query.message.from_user.id)
        if wallet is None:
            return await bot.send_message(chat_id, "you don't have a wallet yet. Tap the button below to create one", reply_markup=quick_markup({
                'Create Wallet': { 'callback_data': queries.Q_CREATE_WALLET},
            }, row_width=1))
        
        data = walletservice.get_tokens_in_wallet(wallet.public_key)
        iterator = filter(lambda x: x["symbol"] == "SOL", data["tokens"])
        balances = [x for x in iterator]
        
        if len(balances) == 0 or balances[0]["totalUiAmount"] <= 0:
            return await bot.send_message(chat_id, common.INSUFFICENT_SOL_BALANCE)
        
        pending_txn = transactionservice.get_pending_txn_by_uid(query.message.from_user.id)
        txn = walletservice.sell_token(wallet.private_key, amount, pending_txn.input_mint)
        if txn is None:
            return await bot.send_message(chat_id, common.TRANSACTION_FAILED)
        
        await bot.send_message(chat_id, common.TRANSACTION_SENT)
    except Exception as e:
        await bot.send_message(chat_id, common.TRANSACTION_FAILED)


async def callback_buy_with_2_sol(bot: AsyncTeleBot, query: CallbackQuery):
    chat_id = query.chat.id
    try:
        amount = 2
        wallet = walletservice.get_wallet_by_telegram_id(query.message.from_user.id)
        if wallet is None:
            return await bot.send_message(chat_id, "you don't have a wallet yet. Tap the button below to create one", reply_markup=quick_markup({
                'Create Wallet': { 'callback_data': queries.Q_CREATE_WALLET},
            }, row_width=1))
        
        data = walletservice.get_tokens_in_wallet(wallet.public_key)
        iterator = filter(lambda x: x["symbol"] == "SOL", data["tokens"])
        balances = [x for x in iterator]
        
        if len(balances) == 0 or balances[0]["totalUiAmount"] <= 0:
            return await bot.send_message(chat_id, common.INSUFFICENT_SOL_BALANCE)
        
        pending_txn = transactionservice.get_pending_txn_by_uid(query.message.from_user.id)
        txn = walletservice.sell_token(wallet.private_key, amount, pending_txn.input_mint)
        if txn is None:
            return await bot.send_message(chat_id, common.TRANSACTION_FAILED)
        
        await bot.send_message(chat_id, common.TRANSACTION_SENT)
    except Exception as e:
        await bot.send_message(chat_id, common.TRANSACTION_FAILED)


async def callback_buy_with_x_sol(bot: AsyncTeleBot, query: CallbackQuery):
    await bot.send_message(query.message.chat.id, replies.ENTER_AMOUNT_OF_SOL_TO_SPEND, reply_markup=ForceReply(input_field_placeholder="0.01234"))


async def callback_confirm_export_pk(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        chat_id = query.message.chat.id
        wallet = walletservice.get_wallet_by_telegram_id(query.from_user.id)
        byte_array = bytes.fromhex(wallet.private_key)
        pk = base58.b58encode(byte_array).decode()
        message = f"Ensure you delete this message immediately you use your private key\n\n`{pk}`"
        await bot.send_message(chat_id, message, reply_markup=quick_markup({
            'Delete Message': {'callback_data': common.Q_GO_BACK}
        }, row_width=1))
        
    except Exception as e:
        print("failed to process cofirm export private key. error: {e}")
        await bot.send_message(chat_id, common.SOMETHING_WENT_WRONG)


async def callback_reset_wallet(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        return
    except Exception as e:
        print("failed to process cofirm export private key. error: {e}")


async def callback_deposit_sol(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        wallet = walletservice.get_wallet_by_telegram_id(query.from_user.id)
        await bot.send_message(query.message.chat.id, f"`{wallet.public_key}`\n👆tap to copy")
    except Exception as e:
        print(f"failed to process callback_deposit_sol. error: {e}")
        await bot.send_message(query.message.chat.id, common.SOMETHING_WENT_WRONG)


async def callback_export_private_key(bot: AsyncTeleBot, query: CallbackQuery):
    chat_id = query.message.chat.id
    await bot.send_message(chat_id, "Never share your private key with anyone. It allows access to your funds. Are you sure you want to export your private key?", reply_markup=quick_markup({
        'Confirm': {'callback_data': queries.Q_CONFIRM_EXPORT_PRIVATE_KEY},
        'Cancel': {'callback_data': common.Q_GO_BACK},
    }, row_width=2))


async def callback_refresh_buy(bot: AsyncTeleBot, query: CallbackQuery):
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
                user_telegram_id=query.from_user.id
            ))
            user_wallet = new_wallet

        tokens = walletservice.get_tokens_in_wallet(user_wallet.public_key)

        iterator = filter(lambda t: t["symbol"] == "SOL", tokens["tokens"])
        matching_tokens = [x for x in iterator]

        if len(matching_tokens) == 0 or matching_tokens[0]["totalUiAmount"] == 0:
            await bot.send_message(chat_id, replies.ZERO_BALANCE_MESSAGE)
            return await bot.send_message(chat_id, user_wallet.public_key)
        
        await bot.send_message(chat_id, replies.BUY_RESPONSE)
        await bot.send_message(chat_id, replies.ENTER_TOKEN_ADDRESS_TO_BUY, reply_markup=ForceReply(input_field_placeholder="4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R"))
    except Exception as e:
        print(f"failed to process buy callback. error: {e}")
        await bot.send_message(chat_id, common.SOMETHING_WENT_WRONG)


async def callback_wallet(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        chat_id = query.message.chat.id
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
        wallet = walletservice.get_wallet_by_telegram_id(query.from_user.id)
        if wallet is None:
            await bot.send_message(chat_id, "You do not have a wallet yet", reply_markup=quick_markup({
                'Create Wallet': {'callback_data': queries.Q_CREATE_WALLET}
            }, row_width=1))
        
        data = walletservice.get_tokens_in_wallet(wallet.public_key)
        iterator = filter(lambda x: x["symbol"] == "SOL", data["tokens"])
        balances = [x for x in iterator]
        sol_balance = 0
        usd_balance = 0
        if (len(balances) == 0):
            sol_balance = 0
            usd_balance = 0
        else:
            sol_balance = balances[0]["totalUiAmount"]
            if not sol_balance == 0:
                price = balances[0]["price"]["usdPrice"] if "price" in balances[0] else 0
                usd_balance = sol_balance * price
        
        message = f"Wallet\n\n*Address*: `{wallet.public_key}`\n(tap to copy)\n\n*Balance (SOL)*: {sol_balance} SOL\n*Balance (USD)*: {usd_balance} USD"
        await bot.send_message(chat_id, message, reply_markup=quick_markup({
            '⬆️ Withdraw x SOL': {'callback_data': queries.Q_WITHDRAW_X_SOL},
            '⬇️ Deposit SOL': {'callback_data': queries.Q_DEPOSIT_SOL},
            '🔃 Reset Wallet': {'callback_data': queries.Q_RESET_WALLET},
            '🔑 Export Private Key': {'callback_data': queries.Q_EXPORT_PRIVATE_KEY},
            '♻️ Refresh': {'callback_data': queries.Q_WALLET},
            '❌ Close': {'callback_data': common.Q_GO_BACK},
        }))
    except Exception as e:
        print(f"failed to process wallet callback query. error: {e}")
        await bot.send_message(chat_id, common.SOMETHING_WENT_WRONG)


async def callback_withdraw_x_sol(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        chat_id = query.message.chat.id
        pendingwithdrawalservice.create_pending_sol_withdrawal(query.from_user.id)
        await bot.send_message(chat_id, replies.ENTER_AMOUNT_OF_SOL_TO_WITHDRAW, reply_markup=ForceReply(input_field_placeholder="0.123"))
    except Exception as e:
        print(f"failed to process withdraw x SOL. error: {e}")
        await bot.send_message(chat_id, common.SOMETHING_WENT_WRONG)
