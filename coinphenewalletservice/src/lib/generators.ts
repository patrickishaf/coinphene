import solanaWeb3 from '@solana/web3.js';

export const generateSolWallet = async function() {
  let wallet = solanaWeb3.Keypair.generate();

  return {
    public_key: wallet.publicKey.toBase58(),
    secret_key: Array.from(wallet.secretKey).map(b => b.toString(16).padStart(2, '0')).join(''),
  };
}
