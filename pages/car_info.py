import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from db.db_utils import get_conn

# ---------------- 지도 좌표 매핑 ----------------
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


# ---------------- 데이터 처리 ----------------
def load_table(table_name: str):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


def normalize_percentage(value):
    try:
        val = float(str(value).replace("%", ""))
        if val <= 1:
            val *= 100
        return round(val, 2)
    except:
        return 0


def process_ev_data():
    df_region = load_table("ev_region_stats")
    df_brand = load_table("ev_brand_stats")

    df_region.rename(columns={"region": "지역", "year": "연도", "elec": "전기차 등록 대수"}, inplace=True)

    total_ev_per_year = df_region.groupby("연도")["전기차 등록 대수"].sum()
    df_region["전국 대비 비율(%)"] = df_region.apply(
        lambda row: round((row["전기차 등록 대수"] / total_ev_per_year.get(row["연도"], 1)) * 100, 2), axis=1
    )

    kia_data = df_brand[df_brand["brand"] == "기아 주식회사"].copy()
    kia_df = pd.DataFrame({
        "연도": [2021, 2022, 2023, 2024],
        "전기차 등록 대수": [kia_data[f"year{y}"].values[0] for y in [2021, 2022, 2023, 2024]],
        "기아 점유율(%)": [normalize_percentage(kia_data[f"year{y}"].values[0]) for y in [2021, 2022, 2023, 2024]]
    })

    return df_region, kia_df


# ---------------- 차트 ----------------
def prepare_donut_chart(df):
    df_2024 = df[df["연도"] == 2024]
    grouped = df_2024.groupby("지역")["전기차 등록 대수"].sum().reset_index()

    fig = go.Figure(data=[go.Pie(
        labels=grouped["지역"],
        values=grouped["전기차 등록 대수"],
        hole=0.6,
        textinfo='label+percent',
        marker=dict(colors=["#C3C3C3"] * len(grouped))
    )])
    fig.update_layout(title_text="지역별 전기차 비율 (2024년)", title_font_size=18)
    return fig


def prepare_kia_chart(kia_df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=kia_df["연도"],
        y=kia_df["전기차 등록 대수"],
        name="전기차 등록대수",
        marker=dict(color="#E1E8FA"),
        yaxis="y1"
    ))

    fig.add_trace(go.Scatter(
        x=kia_df["연도"],
        y=kia_df["기아 점유율(%)"],
        name="기아 점유율",
        mode="lines+markers",
        marker=dict(color="#8D90FF", size=8),
        line=dict(color="#8D90FF", width=2),
        yaxis="y2"
    ))

    fig.update_layout(
        title="기아 전기차 점유율",
        xaxis_title="연도",
        yaxis=dict(title="등록대수", side="left"),
        yaxis2=dict(title="기아 점유율(%)", side="right", overlaying="y", range=[0, 100], showgrid=False),
        legend=dict(orientation="h", x=0.5, y=-0.3),
        bargap=0.3
    )
    return fig


def prepare_fuel_chart(df):
    df["전기차 비율(%)"] = (df["전기차 등록 대수"] / df["전체 차량 등록 대수"] * 100).round(0)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["연도"],
        y=df["전체 차량 등록 대수"],
        name="일반차 등록대수",
        marker=dict(color="#F7EFD1")
    ))
    fig.add_trace(go.Bar(
        x=df["연도"],
        y=df["전기차 등록 대수"],
        name="전기차 등록대수",
        marker=dict(color="#8D90FF")
    ))
    for i, row in df.iterrows():
        fig.add_annotation(
            x=row["연도"],
            y=row["전기차 등록 대수"],
            text=f"{int(row['전기차 비율(%)'])}%",
            showarrow=False,
            font=dict(size=14, color="white"),
            yshift=10
        )

    fig.update_layout(
        barmode="stack",
        title="전기차 등록 비율 (2018~2024년)",
        xaxis_title="연도",
        yaxis_title="등록대수",
        legend=dict(x=0.5, y=-0.2, orientation="h")
    )
    return fig


# ---------------- 메인 ----------------
def show_car_info():
    st.set_page_config(page_title="전기차 대시보드", layout="wide")
    st.title(":car: 전기자동차 지역별 등록 분석")

    df_region, kia_df = process_ev_data()
    df_fuel = load_table("veh_fuel_stats")
    df_fuel.rename(columns={"year": "연도", "total": "전체 차량 등록 대수", "elec": "전기차 등록 대수"}, inplace=True)
    df_fuel = df_fuel[(df_fuel["연도"] >= 2018) & (df_fuel["연도"] <= 2024)]

    top_left, top_right = st.columns(2)
    with top_left:
        st.plotly_chart(prepare_donut_chart(df_region), use_container_width=True)
    with top_right:
        st.plotly_chart(prepare_kia_chart(kia_df), use_container_width=True)

    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        st.markdown("#### 지도에서 지역 선택")
        map_img_path = os.path.join(os.path.dirname(__file__), "pages", "map.png")
        if os.path.exists(map_img_path):
            img = Image.open(map_img_path)
            img = img.resize((500, int(500 * img.height / img.width)))
            value = streamlit_image_coordinates(img, key="map_click")
            if value:
                region = get_region_from_click_px(value['x'], value['y'])
                if region:
                    st.session_state.selected_region = region
                    st.success(f"{region} 선택됨")
        else:
            st.error("지도 이미지를 불러올 수 없습니다.")

    with bottom_right:
        selected = st.session_state.get("selected_region", "전국")
        st.markdown(f"""
            <div style='padding:6px 12px; background:#E0E0E0; border-radius:20px; 
            font-weight:bold; display:inline-block; margin-bottom:8px;'>
            {selected}</div> <span style='font-size:18px'>전기차 등록 및 충전소 분석</span>
        """, unsafe_allow_html=True)
        st.plotly_chart(prepare_fuel_chart(df_fuel), use_container_width=True)


if __name__ == "__main__":
    show_car_info()
