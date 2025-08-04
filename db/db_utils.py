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

def load_car_registration_stats():
    """자동차 등록 통계 데이터 로드"""
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM car_registration_stats", conn)
    conn.close()
    return df

def calculate_ev_ratio_data():
    """DB에서 직접 데이터를 불러와 전기차 비율 계산"""
    
    # 1. 전기차 데이터 로드
    ev_df = load_ev_yearly_stats()
    ev_df = ev_df.rename(columns={'total': 'electric_cars'})
    ev_df['electric_cars'] = ev_df['electric_cars'].astype(int)
    
    # 2. 자동차 등록 데이터 로드 (각 연도별 최신 월 데이터만 필터링)
    car_df = load_car_registration_stats()
    car_df['month'] = car_df['month'].astype(int)
    
    # 각 연도별 최대 월 찾기
    max_months = car_df.groupby('year')['month'].max().reset_index()
    max_months.columns = ['year', 'max_month']
    
    # 각 연도별 최신 월 데이터만 필터링
    car_latest = car_df.merge(max_months, on='year')
    car_latest = car_latest[car_latest['month'] == car_latest['max_month']].copy()
    car_latest = car_latest[['year', 'region', 'total']].rename(columns={'total': 'general_cars'})
    car_latest['general_cars'] = car_latest['general_cars'].astype(int)
    
    # 3. 두 데이터 조인
    merged_df = pd.merge(car_latest, ev_df, on=['year', 'region'], how='inner')
    
    # 4. 전기차 비율 계산
    merged_df['total_cars'] = merged_df['general_cars'] + merged_df['electric_cars']
    merged_df['ev_ratio'] = (merged_df['electric_cars'] / merged_df['total_cars'] * 100).round(2)
    
    # 5. 데이터 정렬
    merged_df = merged_df.sort_values(['year', 'region'])
    
    return merged_df
