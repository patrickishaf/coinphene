import { PublicKey, LAMPORTS_PER_SOL } from "@solana/web3.js"
import { connection } from "./sol.config"
import { TOKEN_2022_PROGRAM_ID, TOKEN_PROGRAM_ID } from "@solana/spl-token"

export const fetchTokenAccounts = async (publicKey: PublicKey) => {
  const result = {
    native_balance: {},
    tokenBalances: [],
  }
  
  const tokenBalances: any[] = []
  const nativeLamports = await connection.getBalance(publicKey)

  result.native_balance = {
    sol: nativeLamports / LAMPORTS_PER_SOL,
    lamports: nativeLamports,
  }

  const tokenAccounts = await connection.getParsedTokenAccountsByOwner(publicKey, { programId: TOKEN_PROGRAM_ID })
  const token2022Accounts = await connection.getParsedTokenAccountsByOwner(publicKey, { programId: TOKEN_2022_PROGRAM_ID })

  tokenAccounts.value.forEach((acc) => {
    const accountData = acc.account.data.parsed.info
    const mint = accountData.mint;  // Token mint address (which token it is)
    const balance = accountData.tokenAmount.uiAmount
    tokenBalances.push({mint, balance})
  })

  token2022Accounts.value.forEach((acc) => {
    const accountData = acc.account.data.parsed.info
    const mint = accountData.mint  // Token mint address (which token it is)
    const balance = accountData.tokenAmount.uiAmount

    tokenBalances.push({mint, balance})
  })

  result.tokenBalances = tokenBalances as never[]
  return result
}
