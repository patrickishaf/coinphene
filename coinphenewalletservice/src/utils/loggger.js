import winston from 'winston';

const manualLogger = winston.createLogger({
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/info.log', level: 'info' }),
    new winston.transports.Console({ level: 'info' })
  ],
});

module.exports = manualLogger;
