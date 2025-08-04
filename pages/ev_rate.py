import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px
from prophet import Prophet
import matplotlib.pyplot as plt

# 제목
st.title("전기차 비율 추이 ( 꺾은선 그래프)")

# DB에서 데이터 불러오기
def get_ev_ratio_data():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='sknproject1',
        charset='utf8mb4'
    )
    query = """
        SELECT year, total, elec
        FROM veh_fuel_stats
        ORDER BY year;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def show_ev_rate():
    # 데이터 불러오기
    df = get_ev_ratio_data()
    df['ev_ratio'] = (df['elec'] / df['total']) * 100

    # Plotly를 이용한 인터랙티브 꺾은선그래프
    fig = px.line(
        df,
        x='year',
        y='ev_ratio',
        title="연도별 전기차 비율 (%)",
        markers=True,
        labels={'year': '연도', 'ev_ratio': '전기차 비율 (%)'},
        line_shape='linear'
    )

    fig.update_layout(yaxis_tickformat=".2f")

    st.plotly_chart(fig, use_container_width=True)

    ##전기차 등록 예측 모델
    predict_data()


def predict_data():
    print(" &&&&&&&& predict Data &&&&&&&&")
    # 1. MySQL 연결
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='sknproject1',
        charset='utf8mb4'
    )

    # 2. 데이터 불러오기
    query = """
        SELECT year, SUM(elec) AS ev
        FROM veh_fuel_stats
        GROUP BY year
        ORDER BY year;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # 3. Prophet 형식으로 컬럼명 변경
    df.rename(columns={'year': 'ds', 'ev': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'], format='%Y')

    # 4. 모델 생성 및 학습
    model = Prophet(yearly_seasonality=True)
    model.fit(df)

    # 5. 향후 3년 데이터 생성 및 예측
    future = model.make_future_dataframe(periods=3, freq='Y')
    forecast = model.predict(future)

    # 6. 결과 출력
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(3))

    # 7. 시각화
    model.plot(forecast)
    plt.title("전기차 등록 예측")
    plt.xlabel("연도")
    plt.ylabel("등록 대수")
    ##plt.show()
    # 예측 시각화
    fig = model.plot(forecast)
    st.pyplot(fig)
