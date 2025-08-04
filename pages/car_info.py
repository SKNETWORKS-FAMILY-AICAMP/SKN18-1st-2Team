import streamlit as st
import plotly.graph_objects as go
from streamlit_image_coordinates import streamlit_image_coordinates
from data_cache import load_ev_stats, process_ev_data, get_total_per_year, load_map_image

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
    """픽셀 좌표 → 지역명 반환"""
    for region, (rx, ry) in region_coords_px.items():
        tol = region_tolerance_px.get(region, 15)
        if abs(x - rx) <= tol and abs(y - ry) <= tol:
            return region
    return None


# ---------------- 차트 함수 ----------------
@st.cache_data(ttl=300)
def prepare_donut_chart(df):
    """2024년 기준 지역별 전기차 등록 비율 도넛"""
    df_2024 = df[df["연도"] == 2024]
    grouped = df_2024.groupby("지역")["전기차 등록 대수"].sum().reset_index()
    total_ev = grouped["전기차 등록 대수"].sum()

    fig = go.Figure(data=[go.Pie(
        labels=grouped["지역"],
        values=grouped["전기차 등록 대수"],
        hole=0.6,
        textinfo='label+percent',
        marker=dict(colors=[
            "#8E97E3", "#FF8C42", "#FFD166", "#06D6A0", "#118AB2", "#EF476F",
            "#073B4C", "#A29BFE", "#FDCB82", "#CDB4DB", "#FFC8DD", "#BDE0FE",
            "#FFADAD", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF"
        ])
    )])
    fig.update_layout(title_text="지역별 전기차 비율 (2024년)")
    return fig


@st.cache_data(ttl=300)
def prepare_kia_chart(df):
    """2021~2024 기아 전기차 점유율"""
    df_filtered = df[(df["연도"] >= 2021) & (df["연도"] <= 2024)]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_filtered["연도"], y=df_filtered["전기차 등록 대수"], name="전기차 등록대수",
        marker=dict(color="#8E97E3")
    ))
    fig.add_trace(go.Scatter(
        x=df_filtered["연도"], y=df_filtered["기아 점유율(%)"], name="기아 점유율", 
        mode="lines+markers", yaxis="y2",
        line=dict(color="#FF8C42", width=3), marker=dict(color="#FF8C42", size=8)
    ))
    fig.update_layout(
        title="기아 전기차 점유율", xaxis_title="연도", yaxis_title="전기차 등록대수",
        yaxis2=dict(title="기아 점유율(%)", overlaying="y", side="right")
    )
    return fig


@st.cache_data(ttl=300)
def prepare_region_chart(filtered_data):
    """지역별 전기차 등록 현황 그래프 (비율 라벨 표시)"""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=filtered_data["연도"], 
        y=filtered_data["전체 차량 등록 대수"], 
        name="전체 차량",
        marker=dict(color="#A0C4FF")
    ))
    fig.add_trace(go.Bar(
        x=filtered_data["연도"], 
        y=filtered_data["전기차 등록 대수"], 
        name="전기차 등록대수",
        marker=dict(color="#8E97E3")
    ))

    # 비율 라벨 추가
    for i, row in filtered_data.iterrows():
        fig.add_annotation(
            x=row["연도"], y=row["전기차 등록 대수"], 
            text=f"{row['전국 대비 비율(%)']}%",
            showarrow=False, font=dict(size=12, color="black"), yshift=10
        )

    fig.update_layout(
        barmode="stack",
        title="지역별 전기차 등록비율 변화",
        xaxis_title="연도",
        yaxis_title="등록대수"
    )
    return fig


# ---------------- 메인 페이지 ----------------
def show_car_info():
    st.set_page_config(page_title="전기자동차 지역별 증가 분석", layout="wide")

    # 데이터 로딩
    try:
        raw_df = load_ev_stats()
        df = process_ev_data()
        total_per_year = get_total_per_year()
    except Exception as e:
        st.error(f"데이터 로딩 오류: {e}")
        st.stop()

    # 지도 로드
    map_img = load_map_image()
    if map_img is None:
        st.error("지도 이미지를 불러올 수 없습니다.")
        st.stop()

    if "selected_region" not in st.session_state:
        st.session_state.selected_region = "전국"

    # ===== 상단 =====
    top_left, top_right = st.columns(2)
    with top_left:
        st.plotly_chart(prepare_donut_chart(df), use_container_width=True)
    with top_right:
        st.plotly_chart(prepare_kia_chart(df), use_container_width=True)

    # ===== 하단 =====
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
        region = st.session_state.selected_region
        filtered = df[(df["지역"] == region) & (df["연도"] >= 2021) & (df["연도"] <= 2024)].copy()

        # 전국 대비 비율 계산
        filtered["전국 대비 비율(%)"] = filtered.apply(
            lambda row: round((row["전기차 등록 대수"] / total_per_year.get(row["연도"], 1)) * 100, 2)
            if total_per_year.get(row["연도"], 0) > 0 else 0, axis=1
        )

        st.plotly_chart(prepare_region_chart(filtered), use_container_width=True)


if __name__ == "__main__":
    show_car_info()
