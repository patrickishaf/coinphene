import dotenv from 'dotenv'

dotenv.config()

const config = {
  port: process.env.PORT,
  fourHorsemen: process.env.FOUR_HORSEMEN?.split(','),
  transactionCharge: Number(process.env.TRANSACTION_CHARGE),
  encryptionKey: process.env.ENCRYPTION_KEY,
  tokenSecret: process.env.TOKEN_SECRET,
  solMint: process.env.SOL_MINT,
  nodeUrl: process.env.NODE_URL,
}

export default config
