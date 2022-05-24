import json
import psycopg2.extras
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
# SET DATABASE
DB_HOSTNAME = os.getenv("HOSTNAME")
DB_PORT = os.getenv('PORT')
DB_NAME = os.getenv('DB')
DB_USER = os.getenv('USER')
DB_PASSWORD = os.getenv('PASS')

# GLOBALS
connection = None
cursor = None

# class to manage database operations in a consistent way


class DatabaseOperation(object):
    def __init__(self):
        self.succeeded = False
        self.error_message = None
        self.query = None
        # records as tuples (no field names)
        self.records = None
        # records as JSON objects with field names (set using the records_to_json method)
        self.json_records = None

    @property
    def record_count(self):
        if self.records == None:
            return 0
        else:
            return len(self.records)

    def __str__(self):
        return 'succeeded:' + str(self.succeeded) + ',error_message:' + str(self.error_message) + ',query:' + str(self.query) + ',records:' + str(self.records)

    def records_to_json(self, field_name_list):
        '''The database routines here return query results as an array of
        arrays, without field names attached.  For JSON responses the field
        names need to be added to each record, which is what this function 
        does.
        - field_name_list - a list of field names as strings.  These will be 
                        applied to each record in the record_list array.
        '''

        if self.records != None and self.record_count > 0:
            json_record = None
            self.json_records = []
            for record in self.records:
                json_record = {}
                for field in range(len(record)):
                    json_record[field_name_list[field]] = record[field]
                    # print(json_record[field_name_list[field]])

                self.json_records.append(json_record)

    def to_json(self):
        succeeded_string = None
        if self.succeeded == True:
            succeeded_string = 'true'
        else:
            succeeded_string = 'false'

        # if the records have been converted to JSON (using records_to_json)
        # then return those.  If they have not, return the records as lists
        output_records = None
        if self.json_records != None:
            output_records = self.json_records
        else:
            # convert tuples in records to lists, since tuples are not valid JSON
            if self.records != None:
                output_records = [list(record_tuple)
                                  for record_tuple in self.records]
            else:
                output_records = []

        # includes the SQL.  Useful for debugging, but should be excluded in production
        # return '{"succeeded":' + succeeded_string + ',"error_message":"' + str(self.error_message) + '","query":' + json.dumps(self.query) + ',"records":' + json.dumps(output_records, default=str) + '}'

        # excludes the SQL
        return '{"succeeded":' + succeeded_string + ',"error_message":"' + str(self.error_message) + '","records":' + json.dumps(output_records, default=str) + '}'


def connect_to_database():
    '''Attempt to connect to the database and acquire a cursor for
    query execution.  Report any failure to the caller along with
    useful information about the error / exception.
    '''
    global cursor
    global connection

    global DB_HOSTNAME, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

    connection_result = DatabaseOperation()

    # safely close existing connections
    close_database_connection()

    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOSTNAME, port=DB_PORT)
        connection.set_session(autocommit=True)
    except Exception as e:
        connection = None
        cursor = None
        connection_result.succeeded = False
        connection_result.error_message = 'Exception while connecting to the database:' + \
            str(e)
        return connection_result

    cursor = None

    try:
        cursor = connection.cursor()
    except Exception as e:
        connection.close()
        connection = None
        cursor = None
        connection_result.succeeded = False
        connection_result.error_message = 'Exception while acquiring a cursor from database connection:' + \
            str(e)
        return connection_result

    connection_result.succeeded = True
    connection_result.error_message = None
    return connection_result


def execute_query(query_sql, query_params=None, execute_many=False):
    '''Acquire a database connection and execute the passed query.
    If a valid database connection is already established this routine
    will use that instead of making a new one.  It will not explicitly
    close the connection however, since keeping a single connection open
    will likely be faster than repeatedly opening and closing one.
    query_sql - The SQL for the actual query, though it may contain
                %s as placeholders for query parameters that
                need to be added.
    query_params - an array of parameters that should be substituted
                for each %s in the query_sql string.  This is the
                method by which substitutions are safely incorporated
                into queries using psycopg2.  This is also the way
                that strings with characters that need to be escaped
                are passed, since Python's escape characters are not
                valid in psycopg2 query specification.
    '''

    global connection
    global cursor

    query_result = DatabaseOperation()

    if connection == None or cursor == None:
        connection_result = connect_to_database()
        if connection_result.succeeded == False:
            query_result.succeeded = False
            query_result.error_message = connection_result.error_message
            return query_result

    cursor_status_message = None
    try:
        # execute many
        if execute_many is True:
            cursor.executemany(query_sql, query_params)
        else:
            cursor.execute(query_sql, query_params)

        cursor_status_message = cursor.statusmessage
        # no longer necessary with autocommit = True
        # connection.commit()
    except Exception as e:
        query_result.succeeded = False
        query_result.error_message = 'Exception while executing query:' + \
            str(e) + ' Query status message:' + \
            str(cursor_status_message) + ' Original query:' + query_sql
        return query_result

    query_result.succeeded = True
    query_result.error_message = None
    if execute_many is False:
        query_result.query = cursor.mogrify(
            query_sql, query_params).decode('utf-8')
    try:
        query_result.records = cursor.fetchall()
    except Exception:
        query_result.records = None

    return query_result


def close_database_connection():
    '''Closes the open database connection and any open cursors.  This is
    necessary because no other routine will close an open database connection;
    a developer will have to call this explicitly when their session is 
    complete.
    '''

    global connection
    global cursor

    if cursor != None:
        cursor.close()
        cursor = None

    if connection != None:
        connection.close()
        connection = None
