import db from "../db"

export enum TransactionType {
  swap = 'swap',
  transfer = 'transfer',
  swapCharges = 'swap_scharges',
  transferCharges = 'transfer_charges'
}

export enum TransactionStatus {
  complete = 'complete',
  pending = 'pending',
  failed = 'failed',
}

export interface Transaction {
  id: number;
  from_address: string
  to_address: string
  amount: number
  type: TransactionType
  timestamp: Date
  status: TransactionStatus
  signature?: string
}

const tableName = 'transactions';

export async function insertTransaction(txn: Partial<Transaction>) {
  const query = db.insert(txn).into(tableName)
  const [id] = await query
  return id
}

export async function findTransactionByProperties(options: Partial<Transaction>) {
  const query = db.select('*').from(tableName).where(options).first()
  const txn = (await query) as Transaction
  return txn
}