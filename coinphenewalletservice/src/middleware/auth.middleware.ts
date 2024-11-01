import { HttpStatusCode } from 'axios'
import config from '../config';
import { NextFunction, Request, Response } from 'express'
import { decrypt } from '../utils';

export default async function ensureUserIsAuthenticated(req: Request, res: Response, next: NextFunction) {
  try {
    const authHeaderEncrypted = req.headers['cp-auth-hdr'];
    const [_, authToken] = decrypt(authHeaderEncrypted! as string).split(' ')
    if (authToken !== config.tokenSecret) return res.status(HttpStatusCode.Unauthorized).json('invalid auth token')
    next()
  } catch (err: any) {
    console.log('failed to authenticate user. error:', err.message)
    return res.status(HttpStatusCode.Unauthorized).json(err.message)
  }
}