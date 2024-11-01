from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, Date, Boolean, Float
from datetime import datetime
from typing import List


class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "users"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    telegram_id = mapped_column(Integer(), nullable=False)
    username = mapped_column(String(90), nullable=False, default="")
    created_at = mapped_column(Date(), default=datetime.now)
    chat_id = mapped_column(Integer(), nullable=True)
    last_modified_at = mapped_column(Date(), default=datetime.now)
    referral_code = mapped_column(String(), nullable=True)

    def __repr__(self):
        return f"User(id={self.id}, telegram_id={self.telegram_id}, username={self.username}, chat_id={self.chat_id}, referral_code={self.referral_code})"


class Wallet(BaseModel):
    __tablename__ = "wallets"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer(), nullable=True)
    user_telegram_id = mapped_column(Integer())
    public_key = mapped_column(String())
    private_key = mapped_column(String())
    balance = mapped_column(Float(), default=0)
    created_at = mapped_column(Date(), default=datetime.now)
    last_modified_at = mapped_column(Date(), nullable=True)

    def __repr__(self):
        return f"Wallet(id={self.id}, public_key={self.public_key}, telegram_id={self.user_telegram_id})"


class UserSettings(BaseModel):
    __tablename__ = "user_settings"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    user_telegram_id = mapped_column(Integer(), nullable=False)
    language = mapped_column(String(), nullable=False, default="en")
    pin_bot = mapped_column(Boolean(), nullable=False, default=False)
    created_at = mapped_column(Date())
    last_modified_at = mapped_column(Date())

    def __repr__(self):
        return f"UserSettings(user_telegram_id={self.user_telegram_id}, language={self.language}, pin_bot={self.pin_bot})"
    

class InChatMessage(BaseModel):
    __tablename__ = "in_chat_messages"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    msg_id = mapped_column(Integer(), nullable=False, default=0)
    chat_id = mapped_column(Integer(), nullable=False, default=0)
    sender_id = mapped_column(Integer(), nullable=False)
    parent_msg_id = mapped_column(Integer(), nullable=True)
    text = mapped_column(String(), nullable=True)
    timestamp = mapped_column(Integer(), nullable=False)

    def __repr__(self) -> str:
        return f"InChatMessage(id={self.id}, msg_id={self.msg_id}, text={self.text}, timestamp={self.timestamp}, chat_id={self.chat_id}, sender_id={self.sender_id}, parent_msg_id={self.parent_msg_id})"


class SplToken(BaseModel):
    __tablename__ = "spl_tokens"

    symbol = mapped_column(String(), nullable=True)
    name = mapped_column(String(), nullable=True)
    address = mapped_column(String(), nullable=False, primary_key=True, autoincrement=False)

    def __repr__(self) -> str:
        return f"SplToken(id={self.id}, symbol={self.symbol}, name={self.name}, address={self.address})"
    

class PendingTransaction(BaseModel):
    __tablename__ = "pending_transactions"

    sender_id = mapped_column(Integer(), primary_key=True)
    type = mapped_column(String(), nullable=True)
    amount = mapped_column(Float(), nullable=True)
    input_mint = mapped_column(String(), nullable=True)
    output_mint = mapped_column(String(), nullable=True)
    input_symbol = mapped_column(String(), nullable=True)
    output_symbol = mapped_column(String(), nullable=True)
    last_updated_at = mapped_column(Date(), default=datetime.now)

    def __repr__(self) -> str:
        return f"CompletedTransaction(id={self.id}, sender_id={self.sender_id}, type={self.type}, amount={self.amount}, input_mint-{self.input_mint}, output_mint={self.output_mint}, input_symbol={self.input_symbol}, output_symbol={self.output_symbol})"


class CompletedTransaction(BaseModel):
    __tablename__ = "completed_transactions"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    sender_id = mapped_column(Integer())
    type = mapped_column(String(), nullable=False)
    amount = mapped_column(Float(), nullable=False)
    input_mint = mapped_column(String(), nullable=False)
    output_mint = mapped_column(String(), nullable=False)
    input_symbol = mapped_column(String(), nullable=False)
    output_symbol = mapped_column(String(), nullable=False)
    hash = mapped_column(String(), nullable=True)
    timestamp = mapped_column(Integer(), nullable=True)

    def __repr__(self) -> str:
        return f"CompletedTransaction(id={self.id}, sender_id={self.sender_id}, type={self.type}, amount={self.amount}, input_mint-{self.input_mint}, output_mint={self.output_mint}, input_symbol={self.input_symbol}, output_symbol={self.output_symbol}, hash={self.hash}, timestamp={self.timestamp})"


class FailedTransaction(BaseModel):
    __tablename__ = "failed_transactions"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    sender_id = mapped_column(Integer())
    type = mapped_column(String(), nullable=False)
    amount = mapped_column(Float(), nullable=False)
    input_mint = mapped_column(String(), nullable=False)
    output_mint = mapped_column(String(), nullable=False)
    input_symbol = mapped_column(String(), nullable=False)
    output_symbol = mapped_column(String(), nullable=False)
    hash = mapped_column(String(), nullable=True)
    timestamp = mapped_column(Integer(), nullable=True)

    def __repr__(self) -> str:
        return f"FailedTransaction(id={self.id}, sender_id={self.sender_id}, type={self.type}, amount={self.amount}, input_mint-{self.input_mint}, output_mint={self.output_mint}, input_symbol={self.input_symbol}, output_symbol={self.output_symbol}, hash={self.hash}, timestamp={self.timestamp})"


class ManagedAsset(BaseModel):
    __tablename__ = "managed_assets"

    user_id = mapped_column(Integer(), primary_key=True, autoincrement=False)
    type = mapped_column(String(), nullable=True)
    ticker = mapped_column(String(), nullable=True)
    amount = mapped_column(Float(), nullable=True)

    def __repr__(self) -> str:
        return f"ManagedAsset(user_id={self.user_id}, type={self.type}, ticker={self.ticker}, amount={self.amount})"


class PendingWithdrawal(BaseModel):
    __tablename__ = "pending_withdrawals"

    user_id = mapped_column(Integer(), primary_key=True, autoincrement=False)
    amount = mapped_column(Float(), nullable=True)
    to_address = mapped_column(String(), nullable=True)
    last_updated_at = mapped_column(Date(), default=datetime.now)

    def __repr__(self) -> str:
        return f"PendingWithdrawal(user_id={self.user_id}, amount={self.amount}, to_address={self.to_address})"


class ReferralCode(BaseModel):
    __tablename__ = "referral_codes"

    owner_tg_id = mapped_column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    code = mapped_column(String(), nullable=False)
    created_at = mapped_column(Date(), default=datetime.now)

    def __repr__(self) -> str:
        return f"ReferralCode(id={self.id}, user_id={self.owner_tg_id}, code={self.code})"
    

class Referral(BaseModel):
    __tablename__ = "referrals"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    referrer_tg_id = mapped_column(Integer(), nullable=False)
    referee_tg_id = mapped_column(Integer(), nullable=False)
    referral_code = mapped_column(String(), nullable=False)

    def __repr__(self) -> str:
        return f"Referral(user_id={self.user_id}, referrer_id={self.referrer_id}, referee_id={self.referee_id}, referral_code={self.referral_code})"
