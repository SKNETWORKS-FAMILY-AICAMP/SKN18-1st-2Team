import pandas as pd
import pymysql

def get_db_connection():
    """DB 연결 함수"""
    return pymysql.connect(
        host='localhost',
        user='root',           
        password='root1234',     
        db='sknproject1',       
        charset='utf8mb4',
        autocommit=True
    )

def insert_car_data_from_csv():
    """CSV 파일에서 자동차 등록 데이터 삽입"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 기존 데이터 삭제
    cursor.execute("TRUNCATE TABLE car_registration_stats")
    print("기존 자동차 등록 데이터 삭제 완료")
    
    # CSV 파일 읽기
    csv_file = 'data/car_registration_stats.csv'
    df = pd.read_csv(csv_file)
    
    print(f"CSV 파일 로드 완료: {len(df)}개 레코드")
    
    # 데이터 삽입
    total_inserted = 0
    
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO car_registration_stats (year, month, region, total)
            VALUES (%s, %s, %s, %s)
        """, (
            str(row['year']), 
            str(row['month']).zfill(2), 
            row['region'], 
            str(row['total'])
        ))
        total_inserted += 1
    
    print(f"삽입 완료: {total_inserted}개 레코드")
    print(f"기간: {df['year'].min()}년 {df['month'].min()}월 ~ {df['year'].max()}년 {df['month'].max()}월")
    print(f"지역: {df['region'].nunique()}개")
    
    conn.close()

if __name__ == "__main__":
    print("CSV에서 자동차 등록 통계 데이터 삽입 시작...")
    insert_car_data_from_csv()
    print("완료!")