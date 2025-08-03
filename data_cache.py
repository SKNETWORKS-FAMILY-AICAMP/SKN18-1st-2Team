import os
import pandas as pd
from PIL import Image
import streamlit as st
from db.db_utils import get_conn

@st.cache_data(ttl=3600)
def load_ev_stats():
    """DB에서 전기차 연도별 통계 불러오기"""
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ev_yearly_stats", conn)
    conn.close()
    return df

@st.cache_data(ttl=3600)
def process_ev_data():
    """데이터 전처리"""
    df = load_ev_stats()
    df_long = df.melt(id_vars=["year"], var_name="지역", value_name="전기차 등록 대수")
    df_long.rename(columns={"year": "연도"}, inplace=True)
    df_long["전기차 등록 대수"] = pd.to_numeric(
        df_long["전기차 등록 대수"].astype(str).str.replace(",", ""),
        errors="coerce"
    )
    df_long["연도"] = pd.to_numeric(df_long["연도"], errors="coerce")
    df_long["전체 차량 등록 대수"] = df_long["전기차 등록 대수"] * 10
    return df_long

@st.cache_data(ttl=3600)
def get_total_per_year():
    """연도별 전국 총계"""
    df_long = process_ev_data()
    return df_long[df_long["지역"] == "전국"].set_index("연도")["전기차 등록 대수"].to_dict()

@st.cache_data(ttl=3600)
def load_map_image():
    """지도 이미지 로딩"""
    # pages 디렉토리의 map.png 파일 경로
    map_img_path = os.path.join(os.path.dirname(__file__), "pages", "map.png")
    if not os.path.exists(map_img_path):
        return None
    map_img = Image.open(map_img_path)
    map_img = map_img.resize((500, int(500 * map_img.height / map_img.width)))
    return map_img
