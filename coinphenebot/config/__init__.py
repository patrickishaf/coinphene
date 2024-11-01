from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
bot_user_id = os.getenv("BOT_USER_ID")
bot_username = os.getenv("BOT_USERNAME")
dummy_wallet_address = os.getenv("DUMMY_WALLET_ADDRESS")
encryption_key = os.getenv("ENCRYPTION_KEY")
native_mint = os.getenv("NATIVE_MINT")
token_secret = os.getenv("TOKEN_SECRET")
txn_charge = float(os.getenv("TRANSACTION_CHARGES"))
wallet_service_url = os.getenv("WALLET_SERVICE_URL")
sentry_url = os.getenv("SENTRY_URL")
logfire_write_token = os.getenv("LOGFIRE_WRITE_TOKEN")
# config = {
#     "bot_token": bot_token,
#     "bot_user_id": bot_user_id,
#     "bot_username": bot_username,
#     "trading_api_key": trading_api_key,
#     "trading_api_key_spot": trading_api_key_spot,
#     "trading_secret_key": trading_secret_key
# }
