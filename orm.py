from fastapi import APIRouter
from dateutil.parser import parse

from sql import sql
import datetime
import database

api = APIRouter(
    prefix="/orm",
    tags=["orm"],
    responses={404: {"message": "Request for a valid orm resource"}}
)


# convert to integer else return false
async def is_integer(strng):
    try:
        return int(strng.strip())
    except ValueError:
        return False
        

# format data
async def format_dict(data_dict):

    # format int properties
    formatted_data = {}
    for key in data_dict:
        try:
            if key == "phone" or "longitude" or "latitude" or "street_address" or "streetaddress":
                formatted_data[key] = data_dict[key].strip()
            else:
                formatted_data[key] = int(data_dict[key].strip())
        except ValueError:
            formatted_data[key] = data_dict[key].strip()

    # return formatted dict
    return formatted_data


# check if string is date
async def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


# insert data into database
async def save(table, data):

    # format int properties
    data = await format_dict(data)
    data["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    data["timestamp_id"] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    data["date_created"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    data["last_modified"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')

    # generate mysql statement
    sql_statement = sql()
    statement = sql_statement.insert_into(table, data).sql_string

    # make database request
    response = await database.orm_async(table, statement, 'list', data)
    
    original_statement = statement # make copy of insert mysql statement
    
    # check if there was an error performing database transaction
    if hasattr(response, 'data_status'):
        
        sql_columns = "" # sql statement
        
        # if table does not exist, create one
        if response.data_code == "table_not_found":
            
            sql_columns = f"{table}_id  INT AUTO_INCREMENT PRIMARY KEY" # primary key
            
            # loop through dictionary to generate database table columns from dictionary keys
            for key in data:
                
                # create columns with data types based on dictionary value
                if isinstance(data[key], int):
                    sql_columns = f"{sql_columns}, {key}  INT"
                if isinstance(data[key], str):
                    sql_columns = f"{sql_columns}, {key}  TEXT"
            
            # add create table to sql statement
            statement = f"CREATE TABLE {table} ({sql_columns})"
            await database.execute_statement(statement)

            # make database request
            response = await database.orm_async(table, original_statement, 'list', data)
            print()
            print(response)
            print()
            
            return response
    
    return response
