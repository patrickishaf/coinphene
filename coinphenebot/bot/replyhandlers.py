from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, ForceReply
from telebot.util import quick_markup
from bot import replies, queries
from tokeninfo import get_token_info, get_token_from_address_cached
import wallet as walletmodule
import config


async def handle_enter_token_address_or_pump_fun_link_to_buy(bot: AsyncTeleBot, message: Message):
    try:
        chat_id = message.chat.id
        token_address = message.text
        if token_address.startswith("https://pump.fun/"):
            token_address = token_address[17:]
            if "pump" in token_address:
                token_address = token_address[:len(token_address) - 4]
        
        print("token address:")
        print(token_address)
        
        # Get data about the token and display to user
        token_info = get_token_info(token_address)
        if token_info is None:
            return await bot.send_message(chat_id, replies.TOKEN_INFO_ERROR_BUY, reply_markup=ForceReply(input_field_placeholder="4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R"))
        
        token_name = token_info["data"]["attributes"]["name"]
        token_symbol = token_info["data"]["attributes"]["symbol"]
        token_address = token_info["data"]["attributes"]["address"]
        token_price_usd = token_info["data"]["attributes"]["price_usd"]
        volume_24h = token_info["data"]["attributes"]["volume_usd"]["h24"]
        market_cap_usd = token_info["data"]["attributes"]["market_cap_usd"]
        # TODO: If the market cap is none, maybe fetch the market cap from somewhere else
        market_cap_usd = 0 if market_cap_usd is None else market_cap_usd
        # 👆 this is a temporary fix


        walletmodule.update_pending_txn_input_mint(message.text, user_id=message.from_user.id)
        walletmodule.update_pending_txn_input_symbol(token_symbol, user_id=message.from_user.id)

        # wallet = walletmodule.get_wallet_by_telegram_id(message.from_user.id)
        # balances = walletmodule.get_tokens_in_wallet(wallet.public_key)
        # iterator = filter(lambda t: t["symbol"] == "SOL", balances["tokens"])
        # matching_tokens = [x for x in iterator]

        # if len(matching_tokens) == 0 or matching_tokens[0]["totalUiAmount"] == 0:
        #     await bot.send_message(chat_id, replies.ZERO_BALANCE_MESSAGE)
        #     return await bot.send_message(chat_id, f"`{wallet.public_key}`")
        
        # sol_balance = matching_tokens[0]["totalUiAmount"]
        result = (f"*{token_name}* | *{token_symbol}*\n\n{token_address}\n\n*Price*: USD {token_price_usd}\n*24h Volume*: USD {volume_24h}\n"
                f"*Market Cap*: USD {market_cap_usd}\n\nTo buy press one of the buttons")
        # Prompt user to to enter the amount to buy
        await bot.send_message(chat_id, result, reply_markup=quick_markup({
                'Buy with 1 SOL': {'callback_data': walletmodule.Q_BUY_WITH_1_SOL},
                'Buy with 2 SOL': {'callback_data': walletmodule.Q_BUY_WITH_2_SOL},
                'Buy with x SOL': {'callback_data': walletmodule.Q_BUY_WITH_X_SOL},
                'Refresh': {'callback_data': walletmodule.Q_REFRESH_BUY},
                'Cancel': {'callback_data': queries.Q_GO_BACK}
            }, row_width=2))
    except Exception as e:
        print(f"failed to process reply handle_token_address_to_buy. error: {e}")
        await bot.send_message(chat_id, replies.SOMETHING_WENT_WRONG)


async def handle_enter_token_address_to_sell(bot: AsyncTeleBot, message: Message):
    chat_id = message.chat.id
    walletmodule.update_pending_txn_output_mint(message.text, message.from_user.id)
    token = get_token_from_address_cached(message.text)
    if token is not None:
        walletmodule.update_pending_txn_output_symbol(token.symbol, message.from_user.id)

    await bot.send_message(chat_id, replies.ENTER_TOKEN_AMOUNT_TO_SELL, reply_markup=ForceReply(input_field_placeholder="0.1234"))


async def handle_enter_token_amount_to_sell(bot: AsyncTeleBot, message: Message):
    try:
        chat_id = message.chat.id
        amount = eval(message.text)
        wallet = walletmodule.get_wallet_by_telegram_id(message.from_user.id)
        pending_txn = walletmodule.get_pending_txn_by_uid(message.from_user.id)
        """
        Ensure that the user has enough token to sell and to pay the transaction charges before sending the transaction request
        """
        txn = walletmodule.sell_token(owner_sk=wallet.private_key, amount=amount, token_address=pending_txn.output_mint)
        if txn is None:
            return await bot.send_message(chat_id, replies.TRANSACTION_FAILED)
        await bot.send_message(chat_id, replies.TRANSACTION_PENDING)
    except Exception as e:
        print(f"failed to sell token. error: {e}")
        await bot.send_message(chat_id, replies.SOMETHING_WENT_WRONG)


async def handle_token_info_error(bot: AsyncTeleBot, message: Message):
    chat_id = message.chat.id
    pass


async def handle_enter_token_symbol(bot: AsyncTeleBot, message: Message):
    # 1. Get the token info
    # 2. Display token info
    # 3. Get user wallet balance
    # 4. Ensure user has a balance
    # 5. (IF USER HAS BALANCE) Display token info
    # 6. (IF USER HAS NO BALANCE) a. Send user wallet address. b. Prompt user to fund wallet
    # 7. Ask user for amount they want to
    # 8. Make the placeholder the maximum amount the user can buy
    await bot.send_message(message.chat.id, replies.ENTER_TOKEN_AMOUNT_TO_BUY, reply_markup=ForceReply(input_field_placeholder="2.0052"))
