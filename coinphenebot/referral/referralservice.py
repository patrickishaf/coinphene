import random
import string
from db import session as db_session, ReferralCode, Referral
import config

def generate_referral_code():
    # define the possible characters (letters and digits)
    characters = string.ascii_letters + string.digits
    # generate a random string by selecting random characters
    code = ''.join(random.choice(characters) for _ in range(5))
    return f"ref_{code}"


def create_referral_link_for_user(user_tg_id: int):
    try:
        existing_code = db_session.query(ReferralCode).where(ReferralCode.owner_tg_id.is_(user_tg_id)).first()
        if existing_code is not None:
            return f"https://t.me/{config.bot_username}?start={existing_code.code}"
        else:
            code = generate_referral_code()
            db_session.add(ReferralCode(owner_tg_id=user_tg_id, code=code))
            db_session.commit()
            return f"https://t.me/{config.bot_username}?start={code}"
    except Exception as e:
        print(f"failed to generate referral link for user. error: {e}")
        return None


async def handle_referral(text: str, user_id: int):
    try:
        # referral link format = ref_Somerandomstring
        code = text.split(" ")[1]
        existing_code = db_session.query(ReferralCode).where(ReferralCode.code.is_(code)).first()

        if existing_code is None:
            return
        
        # create new referral
        db_session.add(Referral(referrer_tg_id=existing_code.owner_tg_id, referee_tg_id=user_id, referral_code=code))
        db_session.commit()
    except Exception as e:
        print("failed to parse the referral link")
