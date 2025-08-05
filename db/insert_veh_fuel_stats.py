import pandas as pd
import pymysql
import os

def insert_veh_fuel():
    conn = pymysql.connect(
        host='localhost',
        user='root',           
        password='root1234',     
        db='sknproject1',       
        charset='utf8mb4'
    )

    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE veh_fuel_stats")
    conn.commit()

    # df = pd.read_csv('../data/veh_fuel_stats.csv')
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "veh_fuel_stats.csv")
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO veh_fuel_stats (year,sorting,total,gasoline,diesel,LPG,hybrid,elec,hydrogen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))
    conn.commit()
    print("veh_fuel_stats 입력 완료")
    conn.close()
