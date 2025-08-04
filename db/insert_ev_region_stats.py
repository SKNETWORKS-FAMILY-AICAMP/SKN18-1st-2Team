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
cursor.execute("TRUNCATE TABLE ev_region_stats")
conn.commit()

df = pd.read_csv('../data/ev_region_stats.csv')   
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO ev_region_stats (region,year,elec,hydrogen,hybrid,eco)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))
conn.commit()
print("ev_region_stats 입력 완료")
conn.close()
