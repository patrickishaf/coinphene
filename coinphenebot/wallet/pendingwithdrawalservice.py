from sqlalchemy import select
from db import PendingWithdrawal, session as db_session
from datetime import datetime


def create_pending_sol_withdrawal(user_id: int):
    try:
        pending_withdrawal = db_session.query(PendingWithdrawal).where(PendingWithdrawal.user_id.is_(user_id)).first()
        if pending_withdrawal is None:
            db_session.add(PendingWithdrawal(user_id=user_id))
            db_session.commit()
        else:
            pending_withdrawal.amount = None
            pending_withdrawal.to_address = None
            db_session.commit()
    except Exception as e:
        print("failed to create new pending sol withdrawal for user")


def get_pending_sol_withdrawal_by_uid(user_id: int):
    try:
        pending_withdrawal = db_session.query(PendingWithdrawal).where(PendingWithdrawal.user_id.is_(user_id)).first()
        return pending_withdrawal
    except Exception as e:
        print(f"failed to get pending sol withdrawal. error: {e}")
        return None
    

def update_pending_sol_withdrawal_amount(amount: float, user_id: int):
    try:
        pending_withdrawal = db_session.query(PendingWithdrawal).where(PendingWithdrawal.user_id.is_(user_id)).first()
        pending_withdrawal.amount = amount
        pending_withdrawal.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update pending sol withdrawal amount. error: {e}")
    

def update_pending_sol_withdrawal_address(address: str, user_id: int):
    try:
        pending_withdrawal = db_session.query(PendingWithdrawal).where(PendingWithdrawal.user_id.is_(user_id)).first()
        pending_withdrawal.to_address = address
        pending_withdrawal.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update pending sol withdrawal to_address. error: {e}")
