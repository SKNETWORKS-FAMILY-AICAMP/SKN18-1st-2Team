import pandas as pd
import pymysql
import os

def insert_ev_brand():
    conn = pymysql.connect(
        host='localhost',
        user='root',           
        password='root1234',     
        db='sknproject1',       
        charset='utf8mb4'
    )

    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE ev_brand_stats")
    conn.commit()

    # df = pd.read_csv('../data/ev_brand_stats.csv')   

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "ev_brand_stats.csv")
    df = pd.read_csv(csv_path) 

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO ev_brand_stats (brand,year,year_rate)
            VALUES (%s, %s, %s)
        """, tuple(row))
    conn.commit()
    print("ev_brand_stats 입력 완료")
    conn.close()
