import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='1234567890',
        database='devOps'
    )
    return connection

def insert_sql(table, data):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            cursor.execute(sql, tuple(data.values()))
            connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        connection.close()


def execute_raw_query(query, params=None):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall() 
            results = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error executing query: {e}")
        results = []
    finally:
        connection.close() 
    return results

