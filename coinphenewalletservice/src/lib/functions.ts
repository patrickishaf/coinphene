import { Transaction, VersionedTransaction, sendAndConfirmTransaction } from '@solana/web3.js'
import { NATIVE_MINT } from '@solana/spl-token'
import axios from 'axios'
import { connection, owner, fetchTokenAccountData } from './sol.config'
import { API_URLS } from '@raydium-io/raydium-sdk-v2'

type SwapCompute = any;

async function getQuote(inputMint: string, outputMint: string, amount: number, slippage: number, txVersion: 'V0' | 'LEGACY') {
  const { data: swapResponse } = await axios.get<SwapCompute>(
    `${API_URLS.SWAP_HOST}/compute/swap-base-in?inputMint=${inputMint}&outputMint=${outputMint}&amount=${amount}&slippageBps=${slippage * 100}&txVersion=${txVersion}`
  ) // Use the URL xxx/swap-base-in or xxx/swap-base-out to define the swap type. 
  return swapResponse;
}

async function serialize(
  swapResponse: ReturnType<typeof getQuote>,
  txVersion: 'V0' | 'LEGACY',
  isInputSol: boolean,
  isOutputSol: boolean,
  inputTokenAcc: typeof owner.publicKey,
  outputTokenAcc: typeof owner.publicKey,
) {
  /**
   * vh: very high
   * h: high
   * m: medium
   */
  const { data } = await axios.get<{
    id: string
    success: boolean
    data: { default: { vh: number; h: number; m: number } }
  }>(`${API_URLS.BASE_HOST}${API_URLS.PRIORITY_FEE}`)
  
  const { data: swapTransactions } = await axios.post<{
    id: string
    version: string
    success: boolean
    data: { transaction: string }[]
  }>(`${API_URLS.SWAP_HOST}/transaction/swap-base-in`, {
    computeUnitPriceMicroLamports: String(data.data.default.h),
    swapResponse,
    txVersion,
    wallet: owner.publicKey.toBase58(),
    wrapSol: isInputSol,
    unwrapSol: isOutputSol, // true means output mint receive sol, false means output mint received wsol
    inputAccount: isInputSol ? undefined : inputTokenAcc?.toBase58(),
    outputAccount: isOutputSol ? undefined : outputTokenAcc?.toBase58(),
  })
  return swapTransactions;
}

async function deserialize(swapTransactions: { data: { transaction: string }[] }, txVersion: 'V0' | 'LEGACY') {
  const isV0Tx = txVersion === 'V0'
  const allTxBuf = swapTransactions.data.map((tx) => Buffer.from(tx.transaction, 'base64'))
  const allTransactions = allTxBuf.map((txBuf) =>
    isV0Tx ? VersionedTransaction.deserialize(txBuf) : Transaction.from(txBuf)
  )

  console.log(`total ${allTransactions.length} transactions`, swapTransactions)
  return allTransactions;
}

async function signAndExecute(txVersion: 'V0' | 'LEGACY', allTransactions: Awaited<ReturnType<typeof deserialize>>) {
  let idx = 0
  const isV0Tx = txVersion === 'V0'
  if (!isV0Tx) {
    for (const tx of allTransactions) {
      console.log(`${++idx} transaction sending...`)
      const transaction = tx as Transaction
      transaction.sign(owner)
      const txId = await sendAndConfirmTransaction(connection, transaction, [owner], { skipPreflight: true })
      console.log(`${++idx} transaction confirmed, txId: ${txId}`)
    }
  } else {
    for (const tx of allTransactions) {
      idx++
      const transaction = tx as VersionedTransaction
      transaction.sign([owner])
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

async function setPriorityFee() {
    // get statistical transaction fee from API
  /**
   * vh: very high
   * h: high
   * m: medium
   */
  const { data } = await axios.get<{
    id: string
    success: boolean
    data: { default: { vh: number; h: number; m: number } }
  }>(`${API_URLS.BASE_HOST}${API_URLS.PRIORITY_FEE}`)

  const { data: swapTransactions } = await axios.post<{
    id: string
    version: string
    success: boolean
    data: { transaction: string }[]
  }>(`${API_URLS.SWAP_HOST}/transaction/swap-base-in`, {
    computeUnitPriceMicroLamports: String(data.data.default.h) // or custom lamport number.
  });

  return swapTransactions;
}