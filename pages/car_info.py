import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import pymysql

# ---------------- DB 연결 ----------------
def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root1234",
        database="sknproject1",
        charset="utf8mb4",
        autocommit=True
    )

# ---------------- DB 테이블 로드 ----------------
def load_table(table_name: str):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# ---------------- 좌표 매핑 ----------------
region_coords_px = {
    "서울": (155,175), "인천": (120,180), "경기": (185,210), "강원": (290,170), 
    "세종": (190,308), "대전": (197,339), "충북": (220,290), "충남": (121,362),
    "광주": (149,500), "전북": (152,444), "전남": (130,545), "제주": (81,715),
    "대구": (339,407), "경북": (325,353), "부산": (385,506), "울산": (416,454), "경남": (272,490)
}
region_tolerance_px = {r: 15 for r in region_coords_px}
region_tolerance_px.update({"강원": 18, "세종": 5, "대전": 10, "제주": 20})


def get_region_from_click_px(x, y):
    for region, (rx, ry) in region_coords_px.items():
        tol = region_tolerance_px.get(region, 15)
        if abs(x - rx) <= tol and abs(y - ry) <= tol:
            return region
    return None

# ---------------- 지도 이미지 로딩 ----------------
def load_map_image():
    """지도 이미지 로드 (pages/map.png)"""
    map_img_path = os.path.join(os.path.dirname(__file__), "map.png")
    if not os.path.exists(map_img_path):
        return None
    map_img = Image.open(map_img_path)
    map_img = map_img.resize((500, int(500 * map_img.height / map_img.width)))
    return map_img

# ---------------- 데이터 전처리 ----------------
def normalize_percentage(value):
    try:
        val = float(str(value).replace("%", ""))
        if val <= 1:
            val *= 100
        return round(val, 2)
    except:
        return 0

def prepare_kia_df(df_brand):
    kia = df_brand[df_brand["brand"] == "기아 주식회사"].iloc[0]
    total = df_brand[df_brand["brand"] == "전체합계"].iloc[0]

    kia_df = pd.DataFrame({
        "연도": [2021, 2022, 2023, 2024],
        "전기차 등록 대수": [total[f"year{y}"] for y in range(2021, 2025)],
        "기아 점유율(%)": [normalize_percentage(kia[f"year{y}_rate"]) for y in range(2021, 2025)]
    })
    return kia_df

# ---------------- 차트 ----------------
def prepare_donut_chart(df_region):
    df_2024 = df_region[df_region["year"] == 2024]
    grouped = df_2024.groupby("region")["elec"].sum().reset_index()

    fig = go.Figure(data=[go.Pie(
        labels=grouped["region"],
        values=grouped["elec"],
        hole=0.6,
        textinfo='label+percent',
        marker=dict(colors=["#A0B9F5", "#FF8C42", "#FFD166", "#06D6A0", "#118AB2",
                            "#EF476F", "#073B4C", "#A29BFE", "#FDCB82", "#CDB4DB", 
                            "#FFC8DD", "#BDE0FE", "#FFADAD", "#FDFFB6", "#CAFFBF", 
                            "#9BF6FF", "#A0C4FF"])
    )])
    fig.update_layout(title_text="지역별 전기차 비율 (2024년)")
    return fig

def prepare_kia_chart(kia_df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=kia_df["연도"],
        y=kia_df["전기차 등록 대수"],
        name="전기차 등록대수",
        marker=dict(color="#A0B9F5")
    ))
    fig.add_trace(go.Scatter(
        x=kia_df["연도"],
        y=kia_df["기아 점유율(%)"],
        name="기아 점유율",
        mode="lines+markers+text",
        text=[f"{v}%" for v in kia_df["기아 점유율(%)"]],
        textposition="top center",
        line=dict(color="#FF8C42", width=3),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title="기아 전기차 점유율",
        xaxis_title="연도",
        yaxis=dict(title="전기차 등록대수", side="left"),
        yaxis2=dict(title="기아 점유율(%)", overlaying="y", side="right", range=[0, 100], showgrid=False),
        legend=dict(x=0.5, y=-0.2, orientation="h")
    )
    return fig

def prepare_fuel_chart(df_fuel):
    df_fuel["전기차 비율(%)"] = (df_fuel["elec"] / df_fuel["total"] * 100).round(0)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_fuel["year"], y=df_fuel["total"], name="일반차 등록대수", marker=dict(color="#FFF3C4")
    ))
    fig.add_trace(go.Bar(
        x=df_fuel["year"], y=df_fuel["elec"], name="전기차 등록대수", marker=dict(color="#A0B9F5")
    ))
    for _, row in df_fuel.iterrows():
        fig.add_annotation(
            x=row["year"], y=row["elec"], text=f"{int(row['전기차 비율(%)'])}%",
            showarrow=False, font=dict(size=14, color="white"), yshift=10
        )
    fig.update_layout(
        barmode="stack", title="전기차 등록 비율 (2018~2024년)",
        xaxis_title="연도", yaxis_title="등록대수",
        legend=dict(x=0.5, y=-0.2, orientation="h")
    )
    return fig

# ---------------- 메인 앱 ----------------
def show_car_info():
    st.set_page_config(page_title="전기자동차 지역별 증가 분석", layout="wide")

    df_region = load_table("ev_region_stats")
    df_brand = load_table("ev_brand_stats")
    df_fuel = load_table("veh_fuel_stats")

    kia_df = prepare_kia_df(df_brand)

    map_img = load_map_image()
    if map_img is None:
        st.error("지도 이미지를 불러올 수 없습니다.")
        st.stop()

    if "selected_region" not in st.session_state:
        st.session_state.selected_region = "전국"

    top_left, top_right = st.columns(2)
    with top_left:
        st.plotly_chart(prepare_donut_chart(df_region), use_container_width=True)
    with top_right:
        st.plotly_chart(prepare_kia_chart(kia_df), use_container_width=True)

    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        st.markdown("#### 지도에서 지역 선택")
        value = streamlit_image_coordinates(map_img, key="map_click")
        if value:
            clicked_region = get_region_from_click_px(value["x"], value["y"])
            if clicked_region:
                st.session_state.selected_region = clicked_region
                st.success(f"{clicked_region} 선택됨")

    with bottom_right:
        st.markdown(f"""
            <div style="display:inline-block; padding:6px 12px; background-color:#E0E0E0; 
            border-radius:20px; font-size:18px; font-weight:bold; color:black;
            margin-right:12px;">
                {st.session_state.selected_region}
            </div>
            <span style="font-size:20px; white-space: nowrap;">
                전기자동차 등록 증가와 충전소 설치 현황 변화 분석
            </span>
        """, unsafe_allow_html=True)

        df_fuel = df_fuel.rename(columns={"year": "year", "total": "total", "elec": "elec"})
        df_fuel = df_fuel[(df_fuel["year"] >= 2018) & (df_fuel["year"] <= 2024)]
        st.plotly_chart(prepare_fuel_chart(df_fuel), use_container_width=True)

if __name__ == "__main__":
    show_car_info()