import { sendSOL, SendSolParams } from './send'
import { apiSwap, SwapParams } from './swap'
import config from '../config'

export async function deductSendCharges(options: SendSolParams) {
  const updatedAmount = (config.transactionCharge / 100) * options.amountOfSOL
  const sendOptions: SendSolParams = {
    amountOfSOL: Math.round(updatedAmount),
    fromKeypair: options.fromKeypair,
    toPubKey: config.fourHorsemen![0],
  }
  const signature = await sendSOL(sendOptions)
  return {signature, amount: Math.round(updatedAmount), to_pk: config.fourHorsemen![0]}
}

export async function deductSolCharges(options: SendSolParams) {
  const updatedAmount = (config.transactionCharge / 100) * options.amountOfSOL
  const promises: Promise<any>[] = []
  config.fourHorsemen?.forEach((publicKey) => {
    promises.push(new Promise((resolve, reject) => {
      const amountOfSOL = updatedAmount / config.fourHorsemen!.length
      const updatedOptions: SendSolParams = { ...options, amountOfSOL, toPubKey: publicKey }
      sendSOL(updatedOptions).then((value) => resolve(value)).catch((err) => reject(err))
    }))
  })
  return Promise.all(promises)
}

async function deductSolExact(options: SendSolParams) {
  const promises: Promise<any>[] = []
  config.fourHorsemen?.forEach((publicKey) => {
    promises.push(new Promise((resolve, reject) => {
      const amountOfSOL = options.amountOfSOL / config.fourHorsemen!.length
      const updatedOptions: SendSolParams = { ...options, amountOfSOL, toPubKey: publicKey }
      sendSOL(updatedOptions).then((value) => resolve(value)).catch((err) => reject(err))
    }))
  })
  return Promise.all(promises)
}

export async function deductTokenCharges(options: SwapParams) {
  try {
    const primaryAddress = config.fourHorsemen![0]
    const chargesAmt = (config.transactionCharge / 100) * options.amt!
    await apiSwap({ ...options, amt: chargesAmt })
    const deductionOptions: SendSolParams = {
      amountOfSOL: chargesAmt,
      fromKeypair: options.ownerKeypair,
      toPubKey: primaryAddress,
    }
    await deductSolExact(deductionOptions)
    const charges = config.transactionCharge
    const updatedAmt = (charges / 100) * options.amt!
    return new Promise((resolve, reject) => {
      const updatedOptions: SwapParams = { ...options, amt: updatedAmt }
      apiSwap(updatedOptions).then((value) => resolve(value)).catch((err) => reject(err))
    })
  } catch (err: any) {
    console.log('failed to deduct token charges. error:', err.message)
    return null
  }
}
