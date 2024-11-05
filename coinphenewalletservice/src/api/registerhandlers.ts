import express, { type Application } from "express"
import cors from 'cors'
import * as controller from "./controller"
import ensureUserIsAuthenticated from "../middleware/auth.middleware"

export async function registerReqHandlers(app: Application) {
  app.use(express.json())
  app.use(express.urlencoded({ extended: true }))
  app.use(cors({origin: true}))
  // app.use('*', ensureUserIsAuthenticated)

  app.post("/keypair/sol", controller.generateSolKeypair)
  app.post("/swap", controller.triggerSwap)
  // app.get("/tokeninfo", getTokenInformation)
  app.get("/balances/:pubkey", controller.getWalletBalance)
  app.get("/sol-balance/:pubkey", controller.getSolBalance)
  app.post("/send-sol", controller.triggerSend)
  app.post("/sell-off", controller.sellOff)
  // app.post("/deduct", deductCharges)
}
