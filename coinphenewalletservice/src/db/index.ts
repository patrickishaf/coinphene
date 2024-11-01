import knex from "knex";
import { attachPaginate} from "knex-paginate";
import knexConfig  from "../../knexfile";

const db = knex(knexConfig);
attachPaginate();

export default db;