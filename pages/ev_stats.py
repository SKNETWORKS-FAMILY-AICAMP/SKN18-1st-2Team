import streamlit as st
import pandas as pd
from db.db_utils import get_conn

def show_ev_stats():
    st.markdown("<h1 style='font-weight:bold;'><span style='font-size:2.5em;'>🚗 자동차 등록 현황</span></h1>", unsafe_allow_html=True)
    st.markdown("##### 전기차 등록현황 표")
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ev_yearly_stats", conn)
    conn.close()
    st.dataframe(df)

    # 연도별 서울 등록대수 그래프
    st.markdown("#### 연도별 서울 전기차 등록대수")
    if "year" in df.columns and "seoul" in df.columns:
        df["year"] = df["year"].astype(str)
        df["seoul_count"] = df["seoul"].str.replace(",", "").str.split().str[0].astype(int)
        st.line_chart(df.set_index("year")["seoul_count"])
    else:
        st.warning("데이터 컬럼명이 맞는지 확인 필요")
