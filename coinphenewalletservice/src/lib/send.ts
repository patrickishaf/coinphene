import { PublicKey, SystemProgram, Transaction, LAMPORTS_PER_SOL, sendAndConfirmTransaction, Keypair } from "@solana/web3.js";
import { connection } from "./sol.config";

export interface SendSolParams {
  amountOfSOL: number
  fromKeypair: Keypair
  toPubKey: string
}

export const sendSOL = async (options: SendSolParams) => {
  const transaction = new Transaction().add(SystemProgram.transfer({
    fromPubkey: options.fromKeypair.publicKey,
    toPubkey: new PublicKey(options.toPubKey),
    lamports: LAMPORTS_PER_SOL * options.amountOfSOL,
  }));
  console.log('transaction created.', transaction);

  const signature = await sendAndConfirmTransaction(connection, transaction, [options.fromKeypair]);
  console.log('transaction signed. signature', signature);

  return signature;
}

export const getWalletBalance = async (pubKey: PublicKey) => {
  const balance = await connection.getBalance(pubKey);

  console.log('balance fetched');
  console.log(balance);

  const bal = {
    sol: balance / LAMPORTS_PER_SOL,
    lamports: balance,
  }

  return bal;
}
