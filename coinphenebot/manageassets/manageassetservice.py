from sqlalchemy import select
from db import ManagedAsset, session as db_session
from datetime import datetime


def create_managed_asset(user_id: int):
    """
    Create a new managed asset if one with the user id does not exist.
    If one exists, set all its fields to None except user_id
    """
    try:
        asset = db_session.query(ManagedAsset).where(ManagedAsset.user_id.is_(user_id)).first()
        if asset is None:
            db_session.add(ManagedAsset(user_id=user_id))
            db_session.commit()
        else:
            asset.amount = None
            asset.ticker = None
            asset.type = None
            db_session.commit()
    except Exception as e:
        print("failed to create new managed asset for user")


def get_managed_asset_by_uid(user_id: int):
    try:
        asset = db_session.query(ManagedAsset).where(ManagedAsset.user_id.is_(user_id)).first()
        return asset
    except Exception as e:
        print(f"failed to get managed asset. error: {e}")
        return None


def update_managed_asset_amount(amount: float, user_id: int):
    try:
        asset = db_session.query(ManagedAsset).where(ManagedAsset.user_id.is_(user_id)).first()
        asset.amount = amount
        asset.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update managed asset amount. error: {e}")


def update_managed_asset_ticker(ticker: str, user_id: int):
    try:
        asset = db_session.query(ManagedAsset).where(ManagedAsset.user_id.is_(user_id)).first()
        asset.ticker = ticker
        asset.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update managed asset ticker. error: {e}")


def update_managed_asset_type(type: str, user_id: int):
    try:
        asset = db_session.query(ManagedAsset).where(ManagedAsset.user_id.is_(user_id)).first()
        asset.type = type.upper()
        asset.last_updated_at = datetime.now()
        db_session.commit()
    except Exception as e:
        print(f"failed to update managed asset type. error: {e}")

