import { Transaction, VersionedTransaction, sendAndConfirmTransaction, Keypair, PublicKey } from '@solana/web3.js'
import { NATIVE_MINT } from '@solana/spl-token'
import axios from 'axios'
import { connection, fetchTokenAccountDataWithAddress } from './sol.config'
import { API_URLS } from '@raydium-io/raydium-sdk-v2'


export interface SwapParams {
  ownerKeypair: Keypair;
  amt?: number;
  inMint?: string;
  outMint?: string;
  slip?: number;
  version?: string;
}

export const apiSwap = async (payload: SwapParams) => {
  const { amt, inMint, outMint, slip, version, ownerKeypair } = payload;
  const inputMint = inMint ? (new PublicKey(inMint)).toBase58() : NATIVE_MINT.toBase58()
  const outputMint = outMint ?? 'Fi6W88vgjx9Qe22Td5A7nSfP6R1z9672obsJ4JmyNf6E' // RAY
  const amount = amt ?? 10
  const slippage = slip ?? 0.5 // in percent, for this example, 0.5 means 0.5%
  const txVersion: string = version ?? 'V0' // or LEGACY
  const isV0Tx = txVersion === 'V0'

  const [isInputSol, isOutputSol] = [inputMint === NATIVE_MINT.toBase58(), outputMint === NATIVE_MINT.toBase58()]

  const { tokenAccounts } = await fetchTokenAccountDataWithAddress(ownerKeypair.publicKey)
  const inputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === inputMint)?.publicKey
  const outputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === outputMint)?.publicKey

  if (!inputTokenAcc && !isInputSol) {
    console.error('do not have input token account')
    return
  }

  // get statistical transaction fee from api
  /**
   * vh: very high
   * h: high
   * m: medium
   */
  interface PriorityFeeResponse {
    id: string
    success: boolean
    data: {
      default: {
        vh: number
        h: number
        m: number
      }
    }
  }
  const { data } = await axios.get<PriorityFeeResponse>(`${API_URLS.BASE_HOST}${API_URLS.PRIORITY_FEE}`)

  interface SwapCompute {
    id: string
    success: true
    version: 'V0' | 'V1'
    openTime?: undefined
    msg: undefined
    data: {
      swapType: 'BaseIn' | 'BaseOut'
      inputMint: string
      inputAmount: string
      outputMint: string
      outputAmount: string
      otherAmountThreshold: string
      slippageBps: number
      priceImpactPct: number
      routePlan: {
        poolId: string
        inputMint: string
        outputMint: string
        feeMint: string
        feeRate: number
        feeAmount: string
      }[]
    }
  }  
  const { data: swapResponse } = await axios.get<SwapCompute>(
    `${
      API_URLS.SWAP_HOST
    }/compute/swap-base-in?inputMint=${inputMint}&outputMint=${outputMint}&amount=${amount}&slippageBps=${
      slippage * 100
    }&txVersion=${txVersion}`
  )

  interface SwapBaseInResponse {
    id: string
    version: string
    success: boolean
    data: { transaction: string }[]
  }
  const { data: swapTransactions } = await axios.post<SwapBaseInResponse>(`${API_URLS.SWAP_HOST}/transaction/swap-base-in`, {
    computeUnitPriceMicroLamports: String(data.data.default.h),
    swapResponse,
    txVersion,
    wallet: ownerKeypair.publicKey.toBase58(),
    wrapSol: isInputSol,
    unwrapSol: isOutputSol, // true means output mint receive sol, false means output mint received wsol
    inputAccount: isInputSol ? undefined : inputTokenAcc?.toBase58(),
    outputAccount: isOutputSol ? undefined : outputTokenAcc?.toBase58(),
  })

  const allTxBuf = swapTransactions.data.map((tx) => Buffer.from(tx.transaction, 'base64'))
  const allTransactions = allTxBuf.map((txBuf) =>
    isV0Tx ? VersionedTransaction.deserialize(txBuf) : Transaction.from(txBuf)
  )

  console.log(`total ${allTransactions.length} transactions`, swapTransactions)

  let idx = 0
  if (!isV0Tx) {
    for (const tx of allTransactions) {
      console.log(`${++idx} transaction sending...`)
      const transaction = tx as Transaction
      transaction.sign(ownerKeypair)
      const txId = await sendAndConfirmTransaction(connection, transaction, [ownerKeypair], { skipPreflight: true })
      console.log(`${++idx} transaction confirmed, txId: ${txId}`)
    }
  } else {
    for (const tx of allTransactions) {
      idx++
      const transaction = tx as VersionedTransaction
      transaction.sign([ownerKeypair])
      const txId = await connection.sendTransaction(tx as VersionedTransaction, { skipPreflight: true })
      const { lastValidBlockHeight, blockhash } = await connection.getLatestBlockhash({
        commitment: 'finalized',
      })
      console.log(`${idx} transaction sending..., txId: ${txId}`)
      await connection.confirmTransaction(
        {
          blockhash,
          lastValidBlockHeight,
          signature: txId,
        },
        'confirmed'
      )
      console.log(`${idx} transaction confirmed`)
    }
  }
}
