import { PublicKey } from '@solana/web3.js';
import { connection } from './sol.config';
import axios from 'axios';

export async function getTokenInfo() {
  const tokenPublicKey = new PublicKey('Fi6W88vgjx9Qe22Td5A7nSfP6R1z9672obsJ4JmyNf6E');
  const tokenInfo = await connection.getParsedAccountInfo(tokenPublicKey);
  const supplyInfo = await connection.getTokenSupply(tokenPublicKey);
  const accountInfo = await connection.getAccountInfo(tokenPublicKey);

  return ({
    tokenInfo: tokenInfo.value?.data,
    tokenInfoParsed: (tokenInfo.value?.data as any).parsed.info,
    supplyInfo,
    accountInfo,
  });
}

export async function getTokenData(tokenId: string) {
  try {
    const url = `https://token-list-api.solana.cloud/v1/search?query=${tokenId.toUpperCase()}&chainId=101&start=0&limit=20`;
    const response = await axios.get(url);
    console.log({ response: response.data.content })
    return response;
  } catch (e: any) {
    console.error(e.message, 'getTokenData');
  }
}