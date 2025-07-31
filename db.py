import pymysql 
import pandas as pd

def get_connection():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='urstory',
        password='1234',
        database='car_db',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )


def get_car_data():
    conn = get_connection()
    try:
        sql = """
        SELECT 
            *
        FROM CarRegistration
        ORDER BY year DESC, month DESC, day DESC
        """
        df = pd.read_sql(sql, conn)
    finally:
        conn.close()
    return df