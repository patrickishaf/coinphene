from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
import bot.replyhandlers as handlers
from bot import replies as botreplies
import manageassets
import wallet

async def route_reply_to_handler(bot: AsyncTeleBot, message: Message):
    parent_message = message.reply_to_message.text

    # Regular replies
    if parent_message == botreplies.ENTER_TOKEN_SYMBOL:
        await handlers.handle_enter_token_symbol(bot, message)
    elif parent_message == botreplies.ENTER_TOKEN_ADDRESS_OR_PUMP_FUN_LINK_TO_BUY:
        await handlers.handle_enter_token_address_or_pump_fun_link_to_buy(bot, message)
    elif parent_message == botreplies.TOKEN_INFO_ERROR_BUY:
        await handlers.handle_token_info_error(bot, message)
    elif parent_message == botreplies.ENTER_TOKEN_ADDRESS_TO_SELL:
        await handlers.handle_enter_token_address_to_sell(bot, message)
    elif parent_message == botreplies.ENTER_TOKEN_AMOUNT_TO_SELL:
        await handlers.handle_enter_token_amount_to_sell(bot, message)
    # Manage Assets Replies
    elif parent_message == manageassets.ENTER_AMOUNT_OF_SOL:
        manageassets.enter_amount_of_token(bot, message)
    elif parent_message == manageassets.ENTER_ASSET_TO_BUY_WITH_X_SOL:
        manageassets.enter_asset_to_buy_with_x_sol(bot, message)
    elif parent_message == manageassets.ENTER_ASSET_TO_SELL_100_PERCENT:
        manageassets.enter_asset_to_sell_100_percent(bot, message)
    elif parent_message == manageassets.ENTER_ASSET_TO_SELL_X_PERCENT:
        manageassets.enter_asset_to_sell_x_percent(bot, message)
    elif parent_message == manageassets.ENTER_PERCENTAGE_OF_TOKEN_TO_SELL:
        pass
    # Wallet replies
    elif parent_message == wallet.ENTER_ADDRESS_TO_WITHDRAW_TO:
        await wallet.handle_enter_address_to_withdraw_to(bot, message)
    elif parent_message == wallet.ENTER_AMOUNT_OF_SOL_TO_SPEND:
        await wallet.handle_enter_amount_of_sol_to_spend(bot, message)
    elif parent_message == wallet.ENTER_AMOUNT_OF_SOL_TO_WITHDRAW:
        await wallet.handle_enter_amount_of_sol_to_withdraw(bot, message)
    else:
        print('unrecognized reply')
        print(message.reply_to_message.text)
        await bot.send_message(message.chat.id, f'unrecognized reply: {message.reply_to_message.text}')