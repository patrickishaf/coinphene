import express, { type Application } from "express"
import cors from 'cors'
import { deductCharges, fetchWalletBalance, generateSolKeypair, getTokenInformation, triggerSwap, triggerSend } from "./controller"
import ensureUserIsAuthenticated from "../middleware/auth.middleware"

export async function registerReqHandlers(app: Application) {
  app.use(express.json())
  app.use(express.urlencoded({ extended: true }))
  app.use(cors({origin: true}))
  app.use('*', ensureUserIsAuthenticated)

  app.post("/keypair/sol", generateSolKeypair)
  app.post("/swap", triggerSwap)
  // app.get("/tokeninfo", getTokenInformation)
  app.get("/balances/:pubkey", fetchWalletBalance)
  app.post("/send-sol", triggerSend)
  // app.post("/deduct", deductCharges)
}
