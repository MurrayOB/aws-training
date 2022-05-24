import src.core.db_operations as db


class Data():
    @staticmethod
    def fetchAll():
        ''' Returns all data. '''
        query_sql = """ SELECT * FROM Node; """
        get_data_result = db.execute_query(query_sql)
        return get_data_result
