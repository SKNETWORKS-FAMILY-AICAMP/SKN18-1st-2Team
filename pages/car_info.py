import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import pymysql
from db.db_utils import load_veh_fuel_stats, load_ev_brand_stats, load_ev_region_stats

# ---------------- DB 연결 ----------------
def prepare_fuel_chart():
    print("prepare_fuel_chart---------------------")

    """veh_fuel_stats → 2018~2024 전기차 비율"""
    df_fuel = load_veh_fuel_stats()

    # 컬럼명 변경
    rename_map = {
        "year": "연도",
        "total": "전체 차량 등록 대수",
        "elec": "전기차 등록 대수"
    }
    df_fuel.rename(columns={old: new for old, new in rename_map.items() if old in df_fuel.columns}, inplace=True)

    # 필수 컬럼 확인
    required_cols = ["연도", "전체 차량 등록 대수", "전기차 등록 대수"]
    if not all(col in df_fuel.columns for col in required_cols):
        st.error(" veh_fuel_stats 테이블 컬럼명이 맞지 않습니다.")
        return go.Figure()

    df_fuel["연도"] = pd.to_numeric(df_fuel["연도"], errors="coerce").fillna(0).astype(int)
    df_fuel = df_fuel[(df_fuel["연도"] >= 2018) & (df_fuel["연도"] <= 2024)]
    df_fuel["전기차 비율(%)"] = (df_fuel["전기차 등록 대수"] / df_fuel["전체 차량 등록 대수"] * 100).round(0)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_fuel["연도"], y=df_fuel["전체 차량 등록 대수"], name="일반차 등록대수", marker=dict(color="#FFF3C4")
    ))
    fig.add_trace(go.Bar(
        x=df_fuel["연도"], y=df_fuel["전기차 등록 대수"], name="전기차 등록대수", marker=dict(color="#A0B9F5")
    ))

    # 비율 라벨 추가
    for _, row in df_fuel.iterrows():
        fig.add_annotation(
            x=row["연도"], y=row["전기차 등록 대수"], 
            text=f"{int(row['전기차 비율(%)'])}%",
            showarrow=False, font=dict(size=14, color="#3665FF", weight="bold"), yshift=10
        )

    fig.update_layout(
        barmode="stack",
        title="전기차 등록 비율 (2018~2024년)",
        xaxis_title="연도",
        yaxis_title="등록대수",
        legend=dict(x=0.5, y=-0.2, orientation="h")
    )
    return fig

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
        print(f"tol 값: {tol}, 타입: {type(tol)}")
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
    try:
        kia = df_brand[df_brand["brand"] == "기아 주식회사"].iloc[0]
        total = df_brand[df_brand["brand"] == "전체합계"].iloc[0]
        
        kia_df = pd.DataFrame({
            "연도": [2021, 2022, 2023, 2024],
            "전기차 등록 대수": [total[f"year{y}"] for y in range(2021, 2025)],
            "기아 점유율(%)": [normalize_percentage(kia[f"year{y}_rate"]) for y in range(2021, 2025)]
        })
        return kia_df
    except Exception as e:
        st.error(f"기아 데이터 처리 오류: {e}")
        # 기본 데이터 반환
        return pd.DataFrame({
            "연도": [2021, 2022, 2023, 2024],
            "전기차 등록 대수": [0, 0, 0, 0],
            "기아 점유율(%)": [0, 0, 0, 0]
        })

# ---------------- 차트 ----------------
def prepare_donut_chart(df_region):
    try:
        df_2024 = df_region[df_region["year"] == 2024]
        if df_2024.empty:
            st.warning("2024년 데이터가 없습니다.")
            return go.Figure()
            
        grouped = df_2024.groupby("region")["elec"].sum().reset_index()

        fig = go.Figure(data=[go.Pie(
            labels=grouped["region"],
            values=grouped["elec"],
            hole=0.6,
            textinfo='label+percent',
            showlegend=False,
            marker=dict(colors=["#A0B9F5", "#FF8C42", "#FFD166", "#06D6A0", "#118AB2",
                                "#EF476F", "#073B4C", "#A29BFE", "#FDCB82", "#CDB4DB", 
                                "#FFC8DD", "#BDE0FE", "#FFADAD", "#FDFFB6", "#CAFFBF", 
                                "#9BF6FF", "#A0C4FF"])
        )])
        fig.update_layout(title_text="지역별 전기차 비율 (2024년)")
        return fig
    except Exception as e:
        st.error(f"도넛 차트 생성 오류: {e}")
        return go.Figure()

def prepare_kia_chart(kia_df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=kia_df["연도"],
        y=kia_df["전기차 등록 대수"],
        name="전기차 등록대수",
        marker=dict(color="#EDF0F9")
    ))
    fig.add_trace(go.Scatter(
        x=kia_df["연도"],
        y=kia_df["기아 점유율(%)"],
        name="기아 점유율",
        mode="lines+markers+text",
        text=[f"{v}%" for v in kia_df["기아 점유율(%)"]],
        textposition="top center",
        line=dict(color="#65ADFF", width=3),
        marker=dict(color="#3665FF", size=8),
        yaxis="y2"
    ))
    fig.update_layout(
        title="기아 전기차 점유율",
        xaxis_title="연도",
        yaxis=dict(title="전기차 등록대수", side="left"),
        yaxis2=dict(title="기아 점유율(%)", overlaying="y", side="right", 
        range=[0, 100], tickvals=list(range(0, 101, 10)), showgrid=False),
        legend=dict(x=0.5, y=-0.2, orientation="h")
    )
    return fig



# ---------------- 메인 앱 ----------------
def show_car_info():
    st.set_page_config(page_title="전기자동차 지역별 증가 분석", layout="wide")

    df_region = load_ev_region_stats()
    df_brand = load_ev_brand_stats()
    df_fuel = load_veh_fuel_stats()

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
                print(f"선택된 지역: {clicked_region}, 타입: {type(clicked_region)}")
                st.session_state.selected_region = clicked_region
                st.success(f"{clicked_region} 선택됨")

    with bottom_right:
        st.markdown(f"""
            <div style="display:inline-block; padding:6px 12px; background-color:#6191FF; 
            border-radius:20px; font-size:18px; font-weight:bold; color:white;
            margin-right:12px;">
                {st.session_state.selected_region}
            </div>
            <span style="font-size:20px; white-space: nowrap;">
                전기자동차 등록 증가와 충전소 설치 현황 변화 분석
            </span>
        """, unsafe_allow_html=True)

        st.plotly_chart(prepare_fuel_chart(), use_container_width=True)

if __name__ == "__main__":
    show_car_info()