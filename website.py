from fastapi import APIRouter

import country
import database
import urllib.parse
from sql import sql

api = APIRouter(
    prefix="/website",
    tags=["website"],
    responses={404: {"message": "Request for a valid resource"}}
)


async def async_profile(country_name: str):
    sql_statement = sql()
    table = 'website_profile'

    country_call_code = urllib.parse.quote_plus(country.country_code_by_name(country_name))

    statement = sql_statement.select(table).where().json_id(table, 'country_call_code', country_call_code).sql_string

    results = await database.orm_async('website_profile', statement, 'dictionary')

    return results


@api.get("/")
def welcome():
    return {
        "message": "You have reached website endpoint, define resources to serve you with",
        "status": "info",
        "data_status": False
    }


@api.get("/country/{country_name}")
def profile(country_name: str):
    sql_statement = sql()
    table = 'website_profile'

    country_call_code = urllib.parse.quote_plus(country.country_code_by_name(country_name))

    statement = sql_statement.select(table).where().json_id(table, 'country_call_code', country_call_code).sql_string

    results = database.orm('website_profile', statement, 'dictionary')

    return results
