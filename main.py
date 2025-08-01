import streamlit as st
from pages.ev_stats import show_ev_stats
from pages.faq import show_faq

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}  /* 자동 생성된 탐색 메뉴 숨김 */
    </style>
""", unsafe_allow_html=True)

# 페이지 기본 설정 - 이 함수는 최상단에 딱 한 번만 호출하세요
st.set_page_config(page_title="기업FAQ", layout="wide")

# 기본 Streamlit 사이드바 사용 (변경 X)
page = st.sidebar.radio("메뉴 선택", ["자동차 등록 현황", "FAQ"])

# 메인 페이지 분기
if page == "자동차 등록 현황":
    show_ev_stats()
elif page == "FAQ":
    show_faq()
