from fastapi import APIRouter
from mysql.connector import connect, Error
import json
import datetime
import timeago
import os
from typing import Dict, List, Any, Optional, Union
from functools import wraps

# Router configuration
api = APIRouter(
    prefix="/database",
    tags=["database"],
    responses={
        404: {"message": "Resource not found"},
        500: {"message": "Database error"}
    }
)

# Database configuration - using original variable names
app_database = "treats_n_more"
host = 'localhost'
user = "root"


# Set password conditionally based on host
def get_db_password() -> str:
    """
    Determine database password based on host:
    - Empty string for localhost
    - 'moi' for any other host
    """
    if host == "localhost" or host == "127.0.0.1":
        return "moi"
    return "moi"


# Custom error class for database operations
class DatabaseError(Exception):
    def __init__(self, message: str, error_code: str = "unknown_error", original_error: Exception = None):
        self.message = message
        self.error_code = error_code
        self.original_error = original_error
        super().__init__(self.message)


# Error mapping function
def map_mysql_error(error: Error) -> DatabaseError:
    """Map MySQL errors to application-specific error codes"""
    error_mapping = {
        2003: ("mysql_server_offline", "Database server is offline or unreachable"),
        1146: ("table_not_found", "The requested table does not exist"),
        1045: ("access_denied", "Access denied: Invalid credentials"),
        1049: ("database_not_found", "Database does not exist"),
        1054: ("unknown_column", "Unknown column in field list"),
    }

    if error.errno in error_mapping:
        code, message = error_mapping[error.errno]
        return DatabaseError(message, code, error)

    return DatabaseError(str(error), "database_error", error)


# Connection management
def get_connection():
    """Create and return a database connection"""
    try:
        return connect(
            host=host,
            user=user,
            password=get_db_password(),
            database=app_database
        )
    except Error as e:
        # Simply return the error as the original code did
        e.data_status = 'error'
        if e.errno and e.errno == 2003:
            e.data_code = 'mysql_server_offline'
        if e.errno and e.errno == 1146:
            e.data_code = 'table_not_found'
        return e


# Connection decorator
def with_connection(func):
    """Decorator to handle database connections"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = get_connection()
            return await func(connection, *args, **kwargs)
        except DatabaseError:
            raise
        except Error as e:
            raise map_mysql_error(e)
        finally:
            if connection and connection.is_connected():
                connection.close()

    return wrapper


# Date and time utilities
def format_date_suffix(day: int) -> str:
    """Return the appropriate ordinal suffix for a day"""
    return 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')


def format_date_with_suffix(date_format: str, date_obj: datetime.datetime) -> str:
    """Format date with ordinal suffix"""
    return date_obj.strftime(date_format).replace('{S}', str(date_obj.day) + format_date_suffix(date_obj.day))


def add_time_metadata(item: Dict[str, Any]) -> Dict[str, Any]:
    """Add time-related metadata to a dictionary"""
    now = datetime.datetime.now()

    # Find timestamp field
    timestamp_field = None
    for field in ('timestamp', 'date_created'):
        if field in item and item[field]:
            timestamp_field = field
            break

    if not timestamp_field:
        return item

    try:
        created_time = datetime.datetime.strptime(item[timestamp_field], '%Y-%m-%d %H:%M:%S')

        # Add time metadata
        item['joined'] = timeago.format(created_time, now)
        item['date_string'] = format_date_with_suffix('%B {S}, %Y', created_time)
    except (ValueError, TypeError):
        # Skip if timestamp format is invalid
        pass

    return item


def process_json_fields(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Process JSON fields in database response"""
    json_field_name = f"{table}_object"

    if json_field_name in data and data[json_field_name]:
        try:
            json_data = json.loads(data[json_field_name])
            # Preserve ID from original data
            if f"{table}_id" in data:
                json_data[f"{table}_id"] = data[f"{table}_id"]
            return json_data
        except json.JSONDecodeError:
            # Return original data if JSON parsing fails
            return data

    return data


def format_response(table: str, data_format: str, response: Any) -> Any:
    """Format database response according to requested format"""
    if not response:
        return [] if data_format == 'list' else None

    if data_format == 'dictionary':
        result = process_json_fields(table, response)
        return add_time_metadata(result)

    if data_format == 'list':
        result = []
        for item in response:
            processed_item = process_json_fields(table, item)
            result.append(add_time_metadata(processed_item))
        return result

    # Default case - return raw response
    return response


# Database operations
@with_connection
async def execute_query(
        connection,
        sql: str,
        params: Optional[List[Any]] = None,
        fetch_one: bool = False
) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
    """Execute a SQL query and return results"""
    cursor = connection.cursor(dictionary=True)
    try:
        # Clean SQL statement
        sql = " ".join(sql.split())

        # Execute query
        cursor.execute(sql, params or [])

        # Return results based on query type
        if sql.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE")):
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()

        # For non-select queries, commit and return affected rows
        connection.commit()
        return {"affected_rows": cursor.rowcount, "last_insert_id": cursor.lastrowid}
    finally:
        cursor.close()


@with_connection
async def execute_insert(
        connection,
        sql: str,
        data: Dict[str, Any]
) -> int:
    """Execute an insert statement and return the last inserted ID"""
    cursor = connection.cursor()
    try:
        # Clean SQL statement
        sql = " ".join(sql.split())

        # Execute query with dictionary values
        cursor.execute(sql, list(data.values()))

        # Commit and return last insert ID
        connection.commit()
        return cursor.lastrowid
    finally:
        cursor.close()


# Original ORM functions with preserved names but improved implementation
def orm(table, sql_statement, data_format, data=None):
    """Object-Relational Mapping function for database operations"""
    password = get_db_password()

    try:
        # connect to mysql database
        with connect(
                host=host,
                user=user,
                password=password,
                database=app_database,
        ) as connection:
            # remove extra spaces in query
            sql_statement = " ".join(sql_statement.split())

            # insert into database
            if data is not None:
                with connection.cursor() as cursor:
                    # Execute with data values
                    cursor.execute(sql_statement, list(data.values()))
                    connection.commit()
                    return cursor.lastrowid
            else:
                # make database query
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(sql_statement)

                    # Format data according to requested format
                    if data_format == 'list':
                        result = format_response(table, data_format, cursor.fetchall())
                    elif data_format == 'dictionary':
                        result = format_response(table, data_format, cursor.fetchone())

                    return result

    except Error as e:
        e.data_status = 'error'
        if e.errno and e.errno == 2003:
            e.data_code = 'mysql_server_offline'
        if e.errno and e.errno == 1146:
            e.data_code = 'table_not_found'
        return e


# Keeping the original function name
async def orm_async(table, sql_statement, data_format, data=None):
    """Asynchronous version of the ORM function"""
    if data is not None:
        database_result = orm(table, sql_statement, data_format, data)
    else:
        database_result = orm(table, sql_statement, data_format)

    return database_result


# Test database connection
def test_mysql_connection() -> bool:
    """Test if database connection can be established"""
    try:
        connection = get_connection()
        result = connection.is_connected()
        connection.close()
        return result
    except (Error, DatabaseError):
        return False


# API Routes
@api.get("/")
def welcome():
    """Welcome endpoint for database API"""
    connection_status = test_mysql_connection()

    return {
        "message": "You have reached database endpoint, define resources to retrieve",
        "status": "info",
        "data_status": False
    }


@api.get("/status")
def status():
    """Database connection status endpoint"""
    connection_status = test_mysql_connection()

    return {
        "status": "online" if connection_status else "offline",
        "database": app_database,
        "host": host,
        "connected": connection_status,
        "config": {
            "host": host,
            "user": user,
            "database": app_database,
            # Don't expose password in response
        }
    }


