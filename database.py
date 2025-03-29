import settings
from mysql.connector import connect, Error

import json
import datetime
import timeago

database_password = '' if settings.global_values['localhost'] else 'moi'
app_database = "treats_n_more"
host = "localhost"
user = "root"


# execute mysql statement
async def execute_statement(sql_statement):
    try:

        # connect to mysql database
        with connect(
                host=host,
                user=user,
                password=database_password,
                database=app_database,
        ) as connection:

            # remove extra spaces in query
            sql_statement = " ".join(sql_statement.split())

            # insert into database
            with connection.cursor() as cursor:
                # valid in Python 2
                # cursor.execute(sql, values.values())

                # valid in Python 3
                cursor.execute(sql_statement)

                # Make sure data is committed to the database
                connection.commit()

                # return last inserted id
                inserted_id = cursor.lastrowid

                # close database connection
                cursor.close()
                connection.close()

                # return database query response
                return inserted_id

    except Error as e:
        e.data_status = 'error'
        if e.errno and e.errno == 2003:
            e.data_code = 'mysql_server_offline'
        if e.errno and e.errno == 1146:
            e.data_code = 'table_not_found'
        return e


# connect to database
def mysql_connection(table, sql_statement, data_format, data=None):
    try:

        # connect to mysql database
        with connect(
                host=host,
                user=user,
                password=database_password,
                database=app_database,
        ) as connection:

            # remove extra spaces in query
            sql_statement = " ".join(sql_statement.split())

            # insert into database
            if data is not None:
                with connection.cursor() as cursor:

                    # valid in Python 2
                    # cursor.execute(sql, values.values())

                    # valid in Python 3
                    cursor.execute(sql_statement, list(data.values()))

                    # Make sure data is committed to the database
                    connection.commit()

                    # return last inserted id
                    inserted_id = cursor.lastrowid

                    cursor.close()
                    connection.close()

                    # return database query response
                    return inserted_id

            else:

                # make database query
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(sql_statement)

                    # format data according to requested format

                    if data_format == 'list':
                        result = format_response(table, data_format, cursor.fetchall())
                    elif data_format == 'dictionary':
                        result = format_response(table, data_format, cursor.fetchone())

                    # return database query response
                    return result

    except Error as e:
        e.data_status = 'error'
        if e.errno and e.errno == 2003:
            e.data_code = 'mysql_server_offline'
        if e.errno and e.errno == 1146:
            e.data_code = 'table_not_found'
        return e


# connect to database
def test_mysql_connection():
    try:
        connection = connect(
            host=host,
            user=user,
            password=database_password,
            database=app_database,
        )
        if connection.is_connected():
            connection.cursor().close()
            connection.close()
            return True

    except Error as e:
        print("Database error")
        print(e)
        return False


def format_response(table, data_format, response):
    if data_format == 'dictionary':
        if response:
            if table + '_object' in response:
                return add_elapsed_time(convert_json_data_to_dictionary(table, response))
            return add_elapsed_time(response)

        return response

    if data_format == 'list':

        if response:

            dictionary_list = []

            for item in response:
                if table + '_object' in item:
                    dictionary_list.append(add_elapsed_time(convert_json_data_to_dictionary(table, item)))

                else:
                    dictionary_list.append(add_elapsed_time(item))

            return dictionary_list

        else:
            return response


def convert_json_data_to_dictionary(table, response):
    json_dictionary = json.loads(response[table + '_object'])
    json_dictionary[table + '_id'] = response[table + '_id']
    return json_dictionary


def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(custom_format, t):
    return t.strftime(custom_format).replace('{S}', str(t.day) + suffix(t.day))


def add_elapsed_time(item):
    timestamp_found = False

    # date strings
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 'timestamp' in item:
        created = item['timestamp']
        timestamp_found = True
    if 'date_created' in item:
        created = item['date_created']
        timestamp_found = True

    if timestamp_found is True:
        date_time_format = '%Y-%m-%d %H:%M:%S'

        # date objects
        now_object = datetime.datetime.strptime(now, date_time_format)
        created_object = datetime.datetime.strptime(created, date_time_format)

        # time elapsed
        item['joined'] = timeago.format(created_object, now_object)

        # date time with suffix e.g 1st May
        item['date_string'] = custom_strftime('%B {S}, %Y', created_object)

    return item


def orm(table, sql_statement, data_format, data=None):
    if data is not None:
        database_result = mysql_connection(table, sql_statement, data_format, data)
    else:
        database_result = mysql_connection(table, sql_statement, data_format)

    return database_result


async def orm_async(table, sql_statement, data_format, data=None):
    if data is not None:
        database_result = mysql_connection(table, sql_statement, data_format, data)
    else:
        database_result = mysql_connection(table, sql_statement, data_format)

    return database_result
