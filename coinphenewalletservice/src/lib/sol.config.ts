import { Raydium, TxVersion, parseTokenAccountResp, publicKey } from '@raydium-io/raydium-sdk-v2'
import { Connection, Keypair, PublicKey, clusterApiUrl } from '@solana/web3.js'
import { TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID } from '@solana/spl-token'
import bs58 from 'bs58'
import config from '../config';

const bytes = Uint8Array.from([55,118,130,152,195,115,244,41,2,244,93,120,238,154,93,40,32,10,161,188,18,119,115,68,187,11,57,191,6,188,40,252,182,170,170,198,235,190,70,100,93,17,94,163,94,59,217,88,80,171,241,94,181,180,115,104,27,108,115,252,101,162,129,177]);
const address = bs58.encode(bytes);
export const owner: Keypair = Keypair.fromSecretKey(bs58.decode(address)) //<YOUR_WALLET_SECRET_KEY>
export const connection = new Connection(config.nodeUrl ?? clusterApiUrl('mainnet-beta')) //<YOUR_RPC_URL>
export const txVersion = TxVersion.V0 // or TxVersion.LEGACY
const cluster = 'mainnet' // 'mainnet' | 'devnet'

let raydium: Raydium | undefined
export const initSdk = async (params?: { loadToken?: boolean }) => {
  if (raydium) return raydium
  console.log(`connect to rpc ${connection.rpcEndpoint} in ${cluster}`)
  raydium = await Raydium.load({
    owner,
    connection,
    cluster,
    disableFeatureCheck: true,
    disableLoadToken: !params?.loadToken,
    blockhashCommitment: 'finalized',
    // urlConfigs: {
    //   BASE_HOST: '<API_HOST>', // api url configs, currently api doesn't support devnet
    // },
  })

  /**
   * By default: sdk will automatically fetch token account data when need it or any sol balace changed.
   * if you want to handle token account by yourself, set token account data after init sdk
   * code below shows how to do it.
   * note: after call raydium.account.updateTokenAccount, raydium will not automatically fetch token account
   */

  /*  
  raydium.account.updateTokenAccount(await fetchTokenAccountData())
  connection.onAccountChange(owner.publicKey, async () => {
    raydium!.account.updateTokenAccount(await fetchTokenAccountData())
  })
  */

  return raydium
}

export const fetchTokenAccountData = async () => {
  const solAccountResp = await connection.getAccountInfo(owner.publicKey)
  const tokenAccountResp = await connection.getTokenAccountsByOwner(owner.publicKey, { programId: TOKEN_PROGRAM_ID })
  const token2022Req = await connection.getTokenAccountsByOwner(owner.publicKey, { programId: TOKEN_2022_PROGRAM_ID })
  const tokenAccountData = parseTokenAccountResp({
    owner: owner.publicKey,
    solAccountResp,
    tokenAccountResp: {
      context: tokenAccountResp.context,
      value: [...tokenAccountResp.value, ...token2022Req.value],
    },
  })
  return tokenAccountData
}

export const fetchTokenAccountDataWithAddress = async (publicKey: PublicKey) => {
  const solAccountResp = await connection.getAccountInfo(publicKey)
  const tokenAccountResp = await connection.getTokenAccountsByOwner(publicKey, { programId: TOKEN_PROGRAM_ID })
  const token2022Req = await connection.getTokenAccountsByOwner(publicKey, { programId: TOKEN_2022_PROGRAM_ID })
  const tokenAccountData = parseTokenAccountResp({
    owner: publicKey,
    solAccountResp,
    tokenAccountResp: {
      context: tokenAccountResp.context,
      value: [...tokenAccountResp.value, ...token2022Req.value],
    },
  })
  return tokenAccountData
}