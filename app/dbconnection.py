import pyodbc

def test_db_connection():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=12.33.65.13;'
        'DATABASE=I-LOG;'
        'UID=sa;'
        'PWD=1qaz!2wsx@'
    )

    try:
        conn = pyodbc.connect(conn_str)
        print("Connection successful!")
        conn.close()
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print("Connection failed. Error: ", sqlstate)

if __name__ == "__main__":
    test_db_connection()
