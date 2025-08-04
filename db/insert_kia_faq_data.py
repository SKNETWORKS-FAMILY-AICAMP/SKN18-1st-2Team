import pandas as pd
import pymysql

def insert_faq_data():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root1234',
        db='sknproject1',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE kia_faq_data")
    conn.commit()

    df = pd.read_csv('../data/kia_faq_data.csv')

    # NaN을 None으로 변환
    df = df.where(pd.notnull(df), None)

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO kia_faq_data (category, question, answer_text, image_urls, link_urls)
            VALUES (%s, %s, %s, %s, %s)
        """, tuple(row))
    conn.commit()
    print("kia_faq_data 입력 완료")
    conn.close()
