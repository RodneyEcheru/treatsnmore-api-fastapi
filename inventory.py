from fastapi import APIRouter

from sql import sql

import database

api = APIRouter(
    prefix='/inventory',
    tags=['inventory'],
    responses={404: {'message': 'Request for a valid resource'}}
)


async def inventory_details_by_country_id(country_id: int):
    sql_statement = sql()
    table = 'inventory'

    statement = sql_statement.select(table).where().id('country_id', country_id).sql_string

    results = database.orm(table, statement, 'list')

    return results


async def inventory_product_details_by_country_id(country_id: int):
    sql_statement = sql()
    table = 'inventory'

    statement = sql_statement.select(table).join('inner', table, 'product_id', 'product', 'product_id').where().id('country_id', country_id).sql_string

    results = database.orm(table, statement, 'list')

    return results


async def inventory_category_product_details_by_country_id(country_id: int):
    sql_statement = sql()
    table = 'inventory'

    statement = sql_statement.select(table).join('inner', table, 'product_id', 'product', 'product_id').join('inner', 'product', 'product_category_id', 'product_category', 'product_category_id').where().id('country_id', country_id).sql_string

    results = database.orm(table, statement, 'list')

    return results


@api.get("/")
def welcome():
    return {
        "message": "You have reached inventory endpoint, define resources to serve you with",
        "status": "info",
        "data_status": False
    }
