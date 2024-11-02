import { PublicKey, LAMPORTS_PER_SOL, GetProgramAccountsFilter } from "@solana/web3.js"
import { connection } from "./sol.config"
import { NATIVE_MINT, TOKEN_2022_PROGRAM_ID, TOKEN_PROGRAM_ID } from "@solana/spl-token"

interface TokenBalance {
  mint: string
  balance: number
}

export interface TokenAccounts {
  native_balance: TokenBalance
  token_balances: TokenBalance[]
}

export const fetchTokenBalances = async (mint: string): Promise<TokenAccounts> => {
  const result: Partial<TokenAccounts> = {
    token_balances: [],
  }

  const publicKey = new PublicKey(mint)
  
  const tokenBalances: TokenBalance[] = []
  const nativeLamports = await connection.getBalance(publicKey)

  result.native_balance = {
    mint: NATIVE_MINT.toString(),
    balance: nativeLamports / LAMPORTS_PER_SOL,
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

  result.token_balances = tokenBalances
  return result as TokenAccounts
}

export const fetchTokenBalancesDetailed = async (wallet: string): Promise<TokenAccounts> => {
  const token_balances: Array<TokenBalance & {[key: string]: any}> = [];
  const nativeLamports = await connection.getBalance(new PublicKey(wallet))

  const native_balance = {
    mint: NATIVE_MINT.toString(),
    balance: nativeLamports / LAMPORTS_PER_SOL,
  }

  const filters: GetProgramAccountsFilter[] = [
    {
      dataSize: 165,    //size of account (bytes)
    },
    {
      memcmp: {
        offset: 32,     //location of our query in the account (bytes)
        bytes: wallet,  //our search criteria, a base58 encoded string
      }            
    }
  ]
  const accounts = await connection.getParsedProgramAccounts(
    TOKEN_PROGRAM_ID,   //SPL Token Program, new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
    {filters: filters}
  )
  accounts.forEach((account, i) => {
    //Parse the account data
    const parsedAccountInfo: any = account.account.data;
    const mintAddress: string = parsedAccountInfo["parsed"]["info"]["mint"]
    const tokenBalance: number = parsedAccountInfo["parsed"]["info"]["tokenAmount"]["uiAmount"]

    token_balances.push({
      account_info: parsedAccountInfo["parsed"]["info"],
      mint: mintAddress,
      balance: tokenBalance,
    })
  })
  return { native_balance, token_balances }
}
