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

region_tolerance_px = {
    "서울": 15, "인천": 15, "경기": 15, "강원": 18, "세종": 5, "대전": 10,
    "충북": 15, "충남": 15, "광주": 15, "전북": 15, "전남": 15, "제주": 20,
    "대구": 15, "경북": 15, "부산": 15, "울산": 15, "경남": 15
}

def get_region_from_click_px(x, y):
    """픽셀 좌표 → 지역명 반환"""
    for region, (rx, ry) in region_coords_px.items():
        tol = region_tolerance_px.get(region, 15)
        if abs(x - rx) <= tol and abs(y - ry) <= tol:
            return region
    return None

@st.cache_data(ttl=300)
def prepare_chart_data(filtered_data, mode):
    """그래프 데이터 준비 (UI 출력 없음)"""
    fig = go.Figure()
    avg_ratio = None
    df_copy = filtered_data.copy()

    if mode == "누적 데이터":
        df_copy["전체 차량 등록 대수"] = df_copy["전체 차량 등록 대수"].cumsum()
        df_copy["전기차 등록 대수"] = df_copy["전기차 등록 대수"].cumsum()
        fig.add_trace(go.Bar(x=df_copy["연도"], y=df_copy["전체 차량 등록 대수"], name="전체 차량"))
        fig.add_trace(go.Scatter(x=df_copy["연도"], y=df_copy["전기차 등록 대수"], name="전기차", mode="lines+markers"))
        avg_ratio = round(df_copy["전국 대비 비율(%)"].mean(), 2)
    else:
        fig.add_trace(go.Bar(x=df_copy["연도"], y=df_copy["전체 차량 등록 대수"], name="전체 차량"))
        fig.add_trace(go.Scatter(x=df_copy["연도"], y=df_copy["전기차 등록 대수"], 
                                 name="전기차", mode="lines+markers", yaxis="y2"))
        fig.add_trace(go.Scatter(x=df_copy["연도"], y=df_copy["전국 대비 비율(%)"], 
                                 name="전국 대비 비율(%)", mode="lines+markers", yaxis="y2"))
        fig.update_layout(yaxis2=dict(title="전국 대비 비율(%)", overlaying="y", side="right"))

    return fig, avg_ratio

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

    # 지도 이미지 로드
    map_img = load_map_image()
    if map_img is None:
        st.error("지도 이미지를 불러올 수 없습니다.")
        st.stop()

    if "selected_region" not in st.session_state:
        st.session_state.selected_region = "전국"

    col1, col2 = st.columns([0.8, 1.2])

    # 지도 클릭
    with col1:
        st.markdown("##### 지도에서 지역 선택")
        value = streamlit_image_coordinates(map_img, key="map_click")
        if value:
            clicked_region = get_region_from_click_px(value["x"], value["y"])
            if clicked_region:
                st.session_state.selected_region = clicked_region
                st.success(f"{clicked_region} 선택됨")

    # 그래프 영역
    with col2:
        region = st.session_state.selected_region

        st.markdown(f"""
            <div style="display:inline-block; padding:6px 12px; background-color:#8E97E3; 
            border-radius:20px; font-size:24px; font-weight:bold; color:white;
            margin-right:12px;">
                {region}
            </div>
            <span style="font-size:20px; white-space: nowrap;">
                전기자동차 등록 증가와 충전소 설치 현황 변화 분석
            </span>
        """, unsafe_allow_html=True)

        filtered = df[
            (df["지역"] == region) &
            (df["연도"] >= 2021) &
            (df["연도"] <= 2024)
        ].copy()

        filtered["전국 대비 비율(%)"] = filtered.apply(
            lambda row: round((row["전기차 등록 대수"] / total_per_year.get(row["연도"], 1)) * 100, 2)
            if total_per_year.get(row["연도"], 0) > 0 else 0,
            axis=1
        )

        chart_fig, avg_ratio = prepare_chart_data(filtered, view_mode)

        if view_mode == "누적 데이터" and avg_ratio is not None:
            st.metric("전국 대비 평균 비율", f"{avg_ratio}%")
        st.plotly_chart(chart_fig, use_container_width=True)

if __name__ == "__main__":
    show_car_info()
