import db from '../db'

export interface Keypair {
  id: number;
  pk: string;
  sk: string;
}

const tableName = 'keypairs';

export async function insertKeypair(keypair: Partial<Keypair>) {
  const query = db.insert(keypair).into(tableName)
  const [id] = await query
  return id
}

export async function findKeypair(options: Partial<Keypair>) {
  const query = db.select('*').from(tableName).where(options).first()
  const txn = (await query) as Keypair
  return txn
}
