import express from 'express'
import { registerReqHandlers } from './api/registerhandlers'
import config from './config'

const port = config.port || 3000
export const server = express()

registerReqHandlers(server)

server.listen(port, () => {
  console.log(`server is running on port ${port}`)
})
