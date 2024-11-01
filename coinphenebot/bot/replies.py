def get_welcome_message(wallet_address: str):
    return (f"Welcome to Coinphene!\n\n\nWe're excited to have you on board! This bot allows you to trade on the "
            f"Solana ecosystem directly within Telegram.\n\n\nTo get started, we've automatically created a new "
            f"wallet for you. Here are the details:\n\n\nWallet Address: `{wallet_address}`\n(tap to "
            f"copy)\n\n\nTo export your private key, click on Wallet > Export Private Key\n\n\nYour Current Balance:"
            f"\n\n\nYou currently have 0 SOL in your "
            f"wallet.\n\n\nGetting Started:\n\n\nTo start trading, deposit SOL to your Coinphene wallet address:"
            f"`{wallet_address}` (tap to copy). once you have SOL in your wallet, you can buy tokens by entering "
            f"the token contract address.\n\n\nNeed Help?\n\n\nFor more information and guides, tap the \"Help\" "
            f"button or ask our support team.\n\n\nWith Coinphene, you can:\n\n\nBuy and sell tokens on the Solana "
            f"blockchain\n\n\nCheck your balance and transaction history\n\n\nGet real-time market updates\n\n\nStay "
            f"tuned for more features and updates!")


def get_return_message(wallet_address: str, balance: float):
    return (f"Welcome back to Coinphene!\n\n\nHere is your wallet address:\n\n\n`{wallet_address}`\n(tap to copy)\n\n\n"
            f"You currently have *{balance} SOL* in your wallet. What would you like to do right now?")


BUY_RESPONSE = "Buy Token:\n\nTo buy a token, enter the symbol, contract address or pump.fun link of the token you want to buy"
ENTER_AMOUNT_OF_SOL_TO_SPEND = "Enter amount of SOL to spend"
ENTER_TOKEN_ADDRESS_OR_PUMP_FUN_LINK_TO_BUY = "Paste the token address or pump.fun link of the token you want to buy"
ENTER_TOKEN_ADDRESS_TO_SELL = "Paste token address to sell"
ENTER_TOKEN_AMOUNT_TO_BUY = "Enter amount of token to buy"
ENTER_TOKEN_AMOUNT_TO_SELL = "Enter amount of token to sell"
ENTER_TOKEN_SYMBOL = "Enter token address or symbol"
SOMETHING_WENT_WRONG = "Something went wrong. Please try again"
TOKEN_INFO_ERROR_BUY = "Invalid token address. Please enter a valid address"
TRANSACTION_FAILED = "Transaction failed. Solana is congested. Consider increasing transaction priority in settings and make sure you have enough SOL to pay for the transaction fee"
TRANSACTION_PENDING = "Transaction sent. Waiting for confirmation...\nIf transaction is slow to confirm, increase transaction priority in /settings. Also make sure you have enough SOL to pay for the transaction fee"
UNRECOGNIZED_TICKER = "Urecognized ticker. Please try again"
ZERO_BALANCE_MESSAGE = "You don't have any SOL to buy tokens with\n\nTo buy a token, please top up your wallet with SOL\n\nADDRESS👇"
