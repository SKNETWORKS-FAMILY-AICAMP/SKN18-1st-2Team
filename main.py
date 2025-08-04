import streamlit as st
from pages.ev_stats import show_ev_stats
from pages.faq import show_faq
from pages.ev_vs_general_comparison import main as show_ev_comparison
from pages.tool_page import show_tool_page

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}  /* 자동 생성된 탐색 메뉴 숨김 */
    </style>
""", unsafe_allow_html=True)

# 페이지 기본 설정 - 이 함수는 최상단에 딱 한 번만 호출하세요
st.set_page_config(page_title="기업FAQ", layout="wide")

# 기본 Streamlit 사이드바 사용 (변경 X)
page = st.sidebar.radio("메뉴 선택", ["자동차 등록 현황", "전기차 vs 일반차 비율 분석", "FAQ", "데이터 도구"])

# 메인 페이지 분기
if page == "자동차 등록 현황":
    show_ev_stats()
elif page == "전기차 vs 일반차 비율 분석":
    show_ev_comparison()
elif page == "FAQ":
    show_faq()
elif page == "데이터 도구":
    show_tool_page()
else:
    st.warning("⚠️ 찾을 수 없는 페이지 입니다. 페이지를 등록해주세요.")
