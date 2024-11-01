import { createCipheriv, createDecipheriv, CipherKey, BinaryLike } from "crypto";
import config from "../config";

function _generateRandomIV() {
  let code = '';
  let possible = '0123456789';

  for (let i = 0; i < 16; i += 1) {
    code += possible.charAt(Math.floor(Math.random() * possible.length));
  }

  return code;
}

export function encrypt(str: string) {
  let randomIV = _generateRandomIV();
  let iv = Buffer.from(randomIV);
  const data = Buffer.from(str);

  const cipher = createCipheriv('aes-256-ctr', config.encryptionKey as CipherKey, iv);
  let encrypted = Buffer.concat([cipher.update(data), cipher.final()]);

  let encryptedHex = encrypted.toString('hex');
  let ivHex = iv.toString('hex');

  return encryptedHex.slice(0, 10) + ivHex + encryptedHex.slice(10, encryptedHex.length);
}

export function decrypt(hash: string) {
  const iv = hash.slice(10, 42);
  const content = hash.slice(0, 10) + hash.slice(42, hash.length);

  const decipher = createDecipheriv('aes-256-ctr', config.encryptionKey as BinaryLike, Buffer.from(iv, 'hex'));
  const decrypted = Buffer.concat([decipher.update(Buffer.from(content, 'hex')), decipher.final()]);

  return decrypted.toString();
}
