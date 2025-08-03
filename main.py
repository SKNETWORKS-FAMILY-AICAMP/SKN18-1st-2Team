import streamlit as st
from pages.car_info import show_car_info
from pages.faq import show_faq

# 성능 최적화를 위한 설정
st.set_page_config(
    page_title="전기차 분석 대시보드",
    layout="wide"
)

# CSS 최적화
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-1oe5cao {display:none;}
.css-6qob1r {display:none;}
[data-testid="stSidebarNav"] {display:none;}

/* 성능 최적화를 위한 추가 CSS */
.stButton > button {
    transition: all 0.3s ease;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# 메뉴 옵션 데이터만 캐싱
@st.cache_data(ttl=3600)
def get_menu_options():
    return ["자동차 등록 현황", "FAQ"]

# 사이드바
def create_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='font-weight:bold;'>Menu</h2>", unsafe_allow_html=True)
        return st.radio("이동", ["자동차 등록 현황", "FAQ"], label_visibility="collapsed")

# 메인 페이지 분기
page = create_sidebar()

if page == "자동차 등록 현황":
    show_car_info()
elif page == "FAQ":
    show_faq()
