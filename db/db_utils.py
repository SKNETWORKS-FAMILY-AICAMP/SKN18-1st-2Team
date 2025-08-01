import pymysql
import pandas as pd

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root1234",  
        database="sknproject1",
        charset="utf8mb4",
        autocommit=True
    )

def load_ev_yearly_stats():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ev_yearly_stats", conn)
    conn.close()
    return df

def load_faq_data():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM kia_faq_data", conn)
    conn.close()
    return df
