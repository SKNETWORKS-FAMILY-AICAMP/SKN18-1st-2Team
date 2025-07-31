import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from db import get_car_data

# ---------------- 데이터 (db.py에서 데이터 연동) ----------------
df = get_car_data()

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="차량 등록 대시보드", layout="wide")

st.title("🚗 차량 등록 현황 대시보드")

# 상단 필터 영역
years = sorted(df["연도"].unique())
regions = sorted(df["지역"].unique())

col1, col2, col3 = st.columns([1.2, 1.2, 1.5])

with col1:
    region = st.selectbox("지역", regions, index=0)

with col2:
    start_year = st.selectbox("시작 연도", years, index=0)
with col3:
    end_year = st.selectbox("종료 연도", years, index=len(years)-1)

# 보기 방식: 개별 vs 누적
view_mode = st.radio(
    "데이터 보기 방식",
    ["개별 연도 데이터", "누적 데이터"],
    horizontal=True
)

# ---------------- 데이터 로딩 및 필터링 ----------------
filtered = df[
    (df["지역"] == region) &
    (df["연도"] >= start_year) &
    (df["연도"] <= end_year)
].copy()

if view_mode == "누적 데이터":
    filtered["전체 차량 등록 대수"] = filtered["전체 차량 등록 대수"].cumsum()
    filtered["전기차 등록 대수"] = filtered["전기차 등록 대수"].cumsum()
else:
    filtered["전체 차량 증가율(%)"] = filtered["전체 차량 등록 대수"].pct_change() * 100
    filtered["전기차 증가율(%)"] = filtered["전기차 등록 대수"].pct_change() * 100

# ---------------- 그래프 ----------------
fig = go.Figure()

# 전체 차량 - 막대그래프
fig.add_trace(go.Bar(
    x=filtered["연도"],
    y=filtered["전체 차량 등록 대수"],
    name="전체 차량 등록 대수",
    marker_color="rgba(255, 225, 100, 0.8)",
))

# 전기차 - 꺾은선 그래프
fig.add_trace(go.Scatter(
    x=filtered["연도"],
    y=filtered["전기차 등록 대수"],
    name="전기차 등록 대수",
    mode="lines+markers",
    line=dict(color="mediumpurple", width=3),
    marker=dict(size=8),
))

# 그래프 스타일 조정
fig.update_layout(
    xaxis_title="연도",
    yaxis_title="등록 대수 (단위: 대)",
    legend=dict(orientation="h", y=-0.2),
    barmode='group',
    margin=dict(t=40, l=40, r=40, b=40),
    height=500,
)

st.plotly_chart(fig, use_container_width=True)