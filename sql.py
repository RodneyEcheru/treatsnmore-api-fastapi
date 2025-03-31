
import datetime


class sql:
    sql_string = ""

    def __init__(self):
        pass

    def select(self, table: str):
        self.sql_string += f"SELECT * FROM {table}"

        return self

    def custom_select(self, arguments: str, table: str):
        self.sql_string += f"SELECT {arguments} FROM {table}"

        return self

    def insert_into(self, table, values: dict):
        values['inserted_timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values['last_modified_timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        placeholders = ', '.join(['%s'] * len(values))
        columns = ', '.join(values.keys())

        self.sql_string += "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)
        return self

    def join(self, join_type: str, primary_table: str, primary_key: str, secondary_table: str, secondary_key: str):
        self.sql_string += " " + join_type.upper() + " JOIN " + secondary_table + " ON " + secondary_table + "." + secondary_key + " = " + primary_table + "." + primary_key
        return self

    def arguments(self, argument: str):
        self.sql_string += " " + argument
        return self

    def limit(self, limit: int):
        self.sql_string += " LIMIT " + str(limit)
        return self

    def paginate(self, offset: int, limit: int):
        self.sql_string += " LIMIT " + str(offset) + ", " + str(limit)
        return self

    def order_by(self, column, order_type):
        self.sql_string += f" ORDER BY {column} {order_type}"
        return self

    def where(self):
        self.sql_string += " WHERE "
        return self

    def and_(self):
        self.sql_string += " AND "
        return self

    def id(self, column_name, value):
        """   f" {column_name} = '{value}' " """
        self.sql_string += ' ' + column_name + ' = "' + str(value) + '" '
        return self

    def json_id(self, table, column_name, value):
        json_column = f"{table}_object"
        # self.sql_string += f'JSON_EXTRACT({table}_object, "$.{column_name}") = "{value}"'
        # self.sql_string += f"JSON_EXTRACT({table}.{table}_object, '$.{column_name}') = '{value}'"
        # self.sql_string += 'json_contains(`'+table+'_object`, `{"'+column_name+'" : "'+value+'"}`)'
        # self.sql_string += "JSON_EXTRACT('{'"+column_name+"':'"+value+"'}', '$."+table+"_object')"
        self.sql_string += ' JSON_EXTRACT(' + json_column + ', "$.' + column_name + '") = "' + value + '"'
        return self
