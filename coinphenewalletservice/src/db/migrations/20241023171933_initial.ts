import type { Knex } from "knex";


export async function up(knex: Knex): Promise<void> {
  return knex.schema.createTable('keypairs', function(table) {
    table.increments('id').primary()
    table.string('pk').unique().notNullable()
    table.string('sk').unique().notNullable
    table.dateTime('created_at').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP'))
  }).createTable('transactions', function(table) {
    table.increments('id').primary()
    table.string('from_address').notNullable()
    table.string('to_address').notNullable()
    table.decimal('amount').notNullable()
    table.string('type').notNullable()
    table.dateTime('timestamp').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP'))
    table.string('status').notNullable()
    table.string('signature').nullable()
    table.dateTime('created_at').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP'))
  })
}


export async function down(knex: Knex): Promise<void> {
  return knex.schema.dropTableIfExists('transactions').dropTableIfExists('keypairs')
}
