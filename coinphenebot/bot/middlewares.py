from db import InChatMessage, session
from telebot.types import Message


def save_message(message: Message):
    try:
        msg_id = message.id
        chat_id = message.chat.id
        sender_id = message.from_user.id
        parent_msg_id = message.reply_to_message.id if message.reply_to_message is not None else None
        text = message.text
        timestamp = message.date

        session.add(InChatMessage(
            msg_id=msg_id,
            chat_id=chat_id,
            sender_id=sender_id,
            parent_msg_id=parent_msg_id,
            text=text,
            timestamp=timestamp
        ))
        session.commit()
    except Exception as e:
        print(f"failed to insert in-chat message into db. error: {e}")