import pandas as pd
import pymysql

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

df = pd.read_csv('../data/ev_yearly_stats_long.csv')   
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO ev_yearly_stats (year, region, total)
        VALUES (%s, %s, %s)
    """, tuple(row))
conn.commit()
print("ev_yearly_stats 입력 완료")
conn.close()
