import { type Knex } from "knex";
import dotenv from 'dotenv';
dotenv.config();

const knexConfig: Knex.Config = {
  client: "sqlite3",
  connection: {
    filename: `./${process.env.DB_NAME}`,
  },
  pool: {
    min: 2,
    max: 10
  },
  migrations: {
    tableName: "knex_migrations",
    directory: "./src/db/migrations"
  },
  seeds: {
    directory: "./src/db/seeds"
  },
  useNullAsDefault: true,
};

export default knexConfig;
