import os
import pandas as pd
import pymysql

def insert_yearly_ev_data():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root1234',
        db='sknproject1',
        charset='utf8mb4'
    )

    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE ev_yearly_stats")
    conn.commit()

    # 현재 파일 기준으로 프로젝트 루트의 data 폴더 내 csv 절대경로 지정
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "ev_yearly_stats_long.csv")
    csv_path = os.path.normpath(csv_path)
    print("읽는 경로:", csv_path)

    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO ev_yearly_stats (year, region, total)
            VALUES (%s, %s, %s)
        """, tuple(row))
    conn.commit()
    print("ev_yearly_stats 입력 완료")
    conn.close()
