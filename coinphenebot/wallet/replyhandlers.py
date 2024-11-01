from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, ForceReply
from telebot.util import quick_markup
from common import replies as common
import wallet.walletservice as walletservice
import wallet.queries as queries
import wallet.transactionservice as transactionservice
import wallet.pendingwithdrawalservice as withdrawalservice
import wallet.replies as replies

async def handle_enter_amount_of_sol_to_spend(bot: AsyncTeleBot, message: Message):
    chat_id = message.chat.id
    try:
        amount = eval(message.text)
        wallet = walletservice.get_wallet_by_telegram_id(message.from_user.id)
        if wallet is None:
            return await bot.send_message(chat_id, "you don't have a wallet yet. Tap the button below to create one", reply_markup=quick_markup({
                'Create Wallet': { 'callback_data': queries.Q_CREATE_WALLET},
            }, row_width=1))
        
        data = walletservice.get_tokens_in_wallet(wallet.public_key)
        iterator = filter(lambda x: x["symbol"] == "SOL", data["tokens"])
        balances = [x for x in iterator]
        
        if len(balances) == 0 or balances[0]["totalUiAmount"] <= 0:
            return await bot.send_message(chat_id, common.INSUFFICENT_SOL_BALANCE)
        
        pending_txn = transactionservice.get_pending_txn_by_uid(message.from_user.id)
        txn = walletservice.buy_token(wallet.private_key, amount, pending_txn.input_mint)
        if txn is None:
            return await bot.send_message(chat_id, common.TRANSACTION_FAILED)
        
        await bot.send_message(chat_id, common.TRANSACTION_SENT)
    except Exception as e:
        print(f"failed to process enter amount of SOL to spend. error: {e}")
        await bot.send_message(chat_id, common.TRANSACTION_FAILED)


async def handle_enter_amount_of_sol_to_withdraw(bot: AsyncTeleBot, message: Message):
    try:
        chat_id = message.chat.id
        amount = eval(message.text)

        wallet = walletservice.get_wallet_by_telegram_id(message.from_user.id)
        data = walletservice.get_tokens_in_wallet(wallet.public_key)
        iterator = filter(lambda x: x["symbol"] == "SOL", data["tokens"])
        balances = [x for x in iterator]

        if len(balances) == 0 or balances[0]["totalUiAmount"] <= 0:
            return await bot.send_message(chat_id, common.INSUFFICENT_SOL_BALANCE)
        
        if amount > balances[0]["totalUiAmount"]:
            await bot.send_message(chat_id, common.INSUFFICENT_SOL_BALANCE)
            return await bot.send_message(chat_id, replies.ENTER_AMOUNT_OF_SOL_TO_WITHDRAW, reply_markup=ForceReply())
        
        withdrawalservice.update_pending_sol_withdrawal_amount(amount, message.from_user.id)
        await bot.send_message(chat_id, replies.ENTER_ADDRESS_TO_WITHDRAW_TO, reply_markup=ForceReply())
    except Exception as e:
        print(f"failed to process enter amount of SOL to withdraw. error: {e}")
        await bot.send_message(chat_id, common.TRANSACTION_FAILED)


async def handle_enter_address_to_withdraw_to(bot: AsyncTeleBot, message: Message):
    # response = (f"Transaction confirmed. \n\n[View on Solana Explorer](https://explorer.solana.com/tx/4qqjzKR1V1gPbthBdvrtRba7VAAWumcMcLcsRPH4My87MyMS36jQpTBGL3GAXuWuFmB5no6ai9EkTAPQSDMGiP7z)"
    #             f"\n\n[View on Solscan](https://solscan.io/tx/4qqjzKR1V1gPbthBdvrtRba7VAAWumcMcLcsRPH4My87MyMS36jQpTBGL3GAXuWuFmB5no6ai9EkTAPQSDMGiP7z)")
    # await bot.send_message(message.chat.id, response)
    try:
        chat_id = message.chat.id
        await bot.send_chat_action(chat_id, 'typing')
        address = message.text

        withdrawalservice.update_pending_sol_withdrawal_address(address, message.from_user.id)
        withdrawal = withdrawalservice.get_pending_sol_withdrawal_by_uid(message.from_user.id)
        wallet = walletservice.get_wallet_by_telegram_id(message.from_user.id)

        txn_signature = walletservice.send_token(address, withdrawal.amount, wallet.private_key)
        if txn_signature is None:
            return await bot.send_message(chat_id, common.TRANSACTION_FAILED)
        
        response = (f"Transaction confirmed. [View on Solana Explorer](https://explorer.solana.com/tx/{txn_signature})"
                    f"[View on Solscan](https://solscan.i0/tx/{txn_signature})")
        await bot.send_message(chat_id, response)
    except Exception as e:
        print(f"failed to process enter addres to withdraw to. error: {e}")
        await bot.send_message(chat_id, common.TRANSACTION_FAILED)
