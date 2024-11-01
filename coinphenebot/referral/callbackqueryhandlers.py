from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
import referral.replies as replies
import referral.referralservice as referralservice
import common.replies as commonreplies

async def callback_refer(bot: AsyncTeleBot, query: CallbackQuery):
    try:
        chat_id = query.message.chat.id
        ref_code = referralservice.create_referral_link_for_user(query.from_user.id)
        if ref_code is None:
            await bot.send_message(chat_id, commonreplies.SOMETHING_WENT_WRONG)
        else:
            await bot.send_message(chat_id, replies.get_ref_link_reply(ref_code, earnings=0, referral_count=0))
    except Exception as e:
        print(f"failed to get referral link for user. error: {e}")
        await bot.send_message(chat_id, commonreplies.SOMETHING_WENT_WRONG)