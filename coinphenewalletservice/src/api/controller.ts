import Joi from 'joi'
import { Request, Response } from 'express'
import { apiSwap, fetchSolBalance, fetchTokenBalances, fetchTokenBalancesDetailed, generateSolWallet, getTokenData, sendSOL, SendSolParams, SwapParams } from '../lib'
import { validateSchema } from '../utils/validateschema'
import { HttpStatusCode } from 'axios'
import { Keypair, PublicKey } from '@solana/web3.js'
import bs58 from 'bs58'
import config from '../config'
import { deductSendCharges, deductSolCharges, deductTokenCharges } from '../lib/charges'
import { insertKeypair } from '../models/keypair'
import { insertTransaction, TransactionStatus, TransactionType } from '../models/transaction'

export async function generateSolKeypair(_: Request, res: Response) {
  try {
    const sol_wallet = await generateSolWallet()
    console.log(sol_wallet)
    await insertKeypair({ pk: sol_wallet.public_key, sk: sol_wallet.secret_key })
    res.status(HttpStatusCode.Created).json(sol_wallet)
  } catch (err) {
    console.log('failed to generate Solana keypair')
    return res.status(HttpStatusCode.InternalServerError).json('failed to create Solana keypair')
  }
}

export async function triggerSwap(req: Request, res: Response) {
  try {
    const schema = Joi.object({
      owner_sk: Joi.string().required(),
      amount: Joi.number().required(),
      input_mint: Joi.string().required(),
      output_mint: Joi.string().required(),
      slippage: Joi.number().optional(),
      tx_version: Joi.string().valid('V0', 'LEGACY').optional()
    })
    const err = await validateSchema(schema, req.body)
    if (err) {
      return res.status(HttpStatusCode.BadRequest).json('failed to execute swap')
    }

    const { owner_sk, amount, input_mint, output_mint, slippage, tx_version = 'V0' } = req.body
    const keyPair = Keypair.fromSecretKey(bs58.decode(bs58.encode(Buffer.from(owner_sk, 'hex'))))

    if (output_mint === config.solMint) {
      // This means that the user wants to send out SOL. This means they have SOL
      const sendOptions: SendSolParams = {
        amountOfSOL: amount,
        fromKeypair: keyPair,
        toPubKey: config.fourHorsemen![0]
      }
      const deduction = await deductSolCharges(sendOptions);
      console.log(deduction);
    } else {
      const deductionOptions: SwapParams = {
        ownerKeypair: keyPair,
        amt: amount,
        inMint: input_mint,
        outMint: output_mint,
      }
      const deduction = await deductTokenCharges(deductionOptions)
      console.log(deduction)
    }

    const data: SwapParams = {
      ownerKeypair: keyPair,
      amt: amount,
      inMint: input_mint,
      outMint: output_mint,
      slip: slippage,
      version: tx_version,
    }

    await apiSwap(data)

    return res.status(HttpStatusCode.Created).json('swap completed')
  } catch (err: any) {
    console.log('failed to do execute swap', err.message)
    return res.status(HttpStatusCode.InternalServerError).json('failed to do execute swap')
  }
}

export async function triggerSend(req: Request, res: Response) {
  try {
    const schema = Joi.object({
      from_secret_key: Joi.string().required(),
      amount: Joi.number().required(),
      to_pub_key: Joi.string().required(),
    });
    const err = await validateSchema(schema, req.body)
    if (err) {
      return res.status(HttpStatusCode.BadRequest).json(err)
    }

    const {amount, from_secret_key, to_pub_key} = req.body
    const fromKeypair = Keypair.fromSecretKey(bs58.decode(bs58.encode(Buffer.from(from_secret_key, 'hex'))))
    const options: SendSolParams = {
      amountOfSOL: Number(amount),
      fromKeypair,
      toPubKey: to_pub_key,
    }

    const charges = await deductSendCharges(options)
    await insertTransaction({
      from_address: fromKeypair.publicKey.toString(),
      to_address: charges.to_pk,
      amount: charges.amount,
      type: TransactionType.transferCharges,
      timestamp: new Date(),
      status: TransactionStatus.complete,
      signature: charges.signature,
    })
    const signature = await sendSOL(options)
    await insertTransaction({
      from_address: fromKeypair.publicKey.toString(),
      to_address: to_pub_key,
      amount: Number(amount),
      type: TransactionType.transfer,
      timestamp: new Date(),
      status: TransactionStatus.complete,
      signature,
    })
    return res.status(HttpStatusCode.Created).json(signature)
  } catch (err: any) {
    console.log('failed to send SOL', err.message)
    const fromKeypair = Keypair.fromSecretKey(bs58.decode(bs58.encode(Buffer.from(req.body.from_secret_key, 'hex'))))
    await insertTransaction({
      from_address: fromKeypair.publicKey.toString(),
      to_address: req.body.to_pub_key,
      amount: Number(req.body.amount),
      type: TransactionType.transfer,
      timestamp: new Date(),
      status: TransactionStatus.complete,
    })
    return res.status(HttpStatusCode.InternalServerError).json('failed to execute swap')
  }
}

export async function getWalletBalance(req: Request, res: Response) {
  try {
    const querySchema = Joi.object({
      detailed: Joi.boolean().optional(),
    })
    const paramSchema = Joi.object({
      pubkey: Joi.string().required(),
    })
    const queryError = await validateSchema(querySchema, req.query)
    const paramsError = await validateSchema(paramSchema, req.params)
    if (queryError || paramsError) {
      return res.status(HttpStatusCode.BadRequest).json(queryError || paramsError)
    }

    const {pubkey} = req.params
    let balances
    if (req.query.detailed) {
      balances = await fetchTokenBalancesDetailed(pubkey!.toString())
    } else {
      balances = await fetchTokenBalances(pubkey!.toString())
    }
    console.log(balances)

    return res.status(HttpStatusCode.Ok).json(balances)
  } catch (err: any) {
    console.log('failed to fetch wallet balance', err.message)
    return res.status(HttpStatusCode.InternalServerError).json('failed to fetch wallet balance')
  }
}

export async function getSolBalance(req: Request, res: Response) {
  try {
    const schema = Joi.object({
      pubkey: Joi.string().required(),
    })
    const error = await validateSchema(schema, req.params)
    if (error) {
      return res.status(HttpStatusCode.BadRequest).json(error)
    }

    const {pubkey} = req.params
    const solBalance = await fetchSolBalance(pubkey)
    console.log(solBalance)

    return res.status(HttpStatusCode.Ok).json(solBalance)
  } catch (err: any) {
    console.log('failed to fetch sol balance', err.message)
    return res.status(HttpStatusCode.InternalServerError).json('failed to fetch SOL balance')
  }
}

export async function getTokenInformation(req: Request, res: Response) {
  try {
    const schema = Joi.object({
      token_symbol: Joi.string().required()
    })
    const err = await validateSchema(schema, req.query)
    if (err) {
      return res.status(HttpStatusCode.BadRequest).json(err)
    }

    const { token_symbol } = req.query
    const info = await getTokenData(token_symbol!.toString())
    return res.status(HttpStatusCode.Ok).json(info);
  } catch (err: any) {
    console.log('failed to get token information', err.message)
    return res.status(HttpStatusCode.InternalServerError).json('failed to get token information')
  }
}

export async function deductCharges(req: Request, res: Response) {
  try {
    if (!config.fourHorsemen || !config.fourHorsemen.length) {
      return res.status(HttpStatusCode.InternalServerError).json('addresses for receiving charges not present')
    }

    const schema = Joi.object({
      from_secret_key: Joi.string().required(),
      amount: Joi.number().required(),
    })
    const err = await validateSchema(schema, req.query)
    if (err) {
      return res.status(HttpStatusCode.BadRequest).json(err)
    }

    let { amount, from_secret_key } = req.body
    amount = Number(amount)
    const keypair = Keypair.fromSecretKey(bs58.decode(from_secret_key))
    const promises: Promise<any>[] = []

    for (let address of config.fourHorsemen) {
      const options: SendSolParams = {
        amountOfSOL: Number(amount),
        fromKeypair: keypair,
        toPubKey: address,
      }

      const promise = new Promise((resolve, reject) => {
        sendSOL(options).then((txn) => resolve(txn)).catch((err) => reject(err))
      })

      promises.push(promise)
    }
    
    const result = Promise.all(promises).catch((err) => {
      throw err
    })

    return res.status(HttpStatusCode.Ok).json(result)
  } catch (err: any) {
    console.log('failed to deduct charges. error:', err.message)
    return res.status(HttpStatusCode.InternalServerError).json('failed to deduct charges from txn')
  }
}

export async function sellOff(req: Request, res: Response) {
  try {
    /**
     * 1. deduct charges
     * 2. get the remaining balance
     * 3. swap the remaining
     */
    return res.status(HttpStatusCode.Ok).json('token sold off')
  } catch (err: any) {
    console.log('failed to sell off token. error:', err.message)
    return res.status(HttpStatusCode.InternalServerError).json('failed to sell off token')
  }
}