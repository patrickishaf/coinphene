from db import User, session as db_session


def save_user(telegram_id: int, username: str, chat_id: int, referral_code: str = None):
    """
    :param telegram_id: integer representing telegram id of user.
    :type telegram_id: :obj:`int`

    :param username: string representing the username of the user.
    :type username: :obj:`str`

    :param chat_id: string representing the chat id of the user
    :type chat_id: :obj:`str`

    :param referral_code: string representing the referral code of the user
    :type referral_code: :obj:`str`
    """
    try:
        user = User(
            telegram_id=telegram_id,
            username=username,
            chat_id=chat_id,
            referral_code=referral_code
        )
        db_session.add(user)
        db_session.commit()
    except Exception as e:
        print(f"failed to create user. error {e}")


def get_user_by_tg_id(telegram_id: int):
    """
    :param telegram_id: integer representing telegram id of the user
    :type telegram_id: :obj:`str`
    """
    try:
        user = db_session.query(User).where(User.telegram_id.is_(telegram_id)).first()
        return user
    except Exception as e:
        print(f"failed to get user by telegram id. error: {e}")
        return None
