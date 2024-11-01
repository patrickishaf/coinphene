from sqlalchemy import select
from db import PendingTransaction, session as db_session
from datetime import datetime


def create_pending_txn(user_id: int):
    try:
        db_session.add(PendingTransaction(sender_id=user_id))
        db_session.commit()
    except Exception as e:
        print("failed to create new pending transaction for user")


def get_pending_txn_by_uid(user_id: int):
    try:
        txn = db_session.query(PendingTransaction).where(PendingTransaction.sender_id.is_(user_id)).first()
        return txn
    except Exception as e:
        print(f"failed to get pending transaction. error: {e}")
        return None
    

def update_pending_txn_type(type: str, user_id: int):
    try:
        txn = db_session.query(PendingTransaction).where(PendingTransaction.sender_id.is_(user_id)).first()
        txn.type = type.upper()
        txn.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update pending txn type. error: {e}")
    

def update_pending_txn_amount(amount: float, user_id: int):
    try:
        txn = db_session.query(PendingTransaction).where(PendingTransaction.sender_id.is_(user_id)).first()
        txn.amount = amount
        txn.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update pending txn amount. error: {e}")
    

def update_pending_txn_input_mint(input_mint: str, user_id: int):
    try:
        txn = db_session.query(PendingTransaction).where(PendingTransaction.sender_id.is_(user_id)).first()
        txn.input_mint = input_mint
        txn.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update pending txn input mint. error: {e}")
    

def update_pending_txn_output_mint(output_mint: str, user_id: int):
    try:
        txn = db_session.query(PendingTransaction).where(PendingTransaction.sender_id.is_(user_id)).first()
        txn.output_mint = output_mint
        txn.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update pending txn output mint. error: {e}")
    

def update_pending_txn_input_symbol(input_symbol: str, user_id: int):
    try:
        txn = db_session.query(PendingTransaction).where(PendingTransaction.sender_id.is_(user_id)).first()
        txn.input_symbol = input_symbol
        txn.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update pending txn input symbol. error: {e}")
    

def update_pending_txn_output_symbol(output_symbol: str, user_id: int):
    try:
        txn = db_session.query(PendingTransaction).where(PendingTransaction.sender_id.is_(user_id)).first()
        txn.output_symbol = output_symbol
        txn.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update pending txn output symbol. error: {e}")
    