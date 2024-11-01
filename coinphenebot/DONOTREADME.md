The Endpoint we use for getting tokens in a solana address comes from solana's solflare wallet. If it changes we must update it

# URLS WE NEED TO MONITOR FOR CHANGES
getTokenImage
getTokensInSolanaAddress

# Important Things To Do

Each time you fetch data about a token with its address, save the token information like symbol, address and market cap in the db or preferably cache for easy lookup so that we won't need to use the API repeatedly for basic things

Each time a user starts using the bot, I have to save their chat id to the user object itself. So that the bot can send messages to a user at any time. This will be helpful in notifying users about their transaction status

Each time a user or the bot sends a message, save the message to db. It is absolutely important so that the bot can delete messages

Pass a particular token (not the bot token) in the header of every request to the server. The backend will need it to be present to authenticate requests

Encrypt the secret keys that we are sending via the API calls