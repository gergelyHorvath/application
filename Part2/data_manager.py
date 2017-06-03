import psycopg2


def get_connection_data(filename="priveate_connection_data.txt"):
    with open(filename, 'r') as file:
        data = file.read().splitlines()
        return(data)


def run_query(sql_query):
    connect_data = get_connection_data()
    try:
        connect_str = "dbname='{}' user='{}' host='{}' password='{}'".format(*connect_data)
        connection = psycopg2.connect(connect_str)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(sql_query)
        data_table = cursor.fetchall()
        cursor.close()
    except psycopg2.DatabaseError as exception:
        print(exception)
    finally:
        if connection:
            connection.close()
    return data_table

# sql_q = "select * from mentors"
# print(run_query(sql_q))