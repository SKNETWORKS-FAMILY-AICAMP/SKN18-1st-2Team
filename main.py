import streamlit as st
from pages.ev_stats import show_ev_stats
from pages.faq import show_faq


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-1oe5cao {display:none;} /* navigation menu */
            .css-6qob1r {display:none;} /* new sidebar class */
            [data-testid="stSidebarNav"] {display:none;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 레이아웃, 기본 설정
st.set_page_config(page_title="기업FAQ", layout="wide")

# 커스텀 사이드바
with st.sidebar:
    st.markdown("<h2 style='font-weight:bold;'>Menu</h2>", unsafe_allow_html=True)
    page = st.radio("이동", ["자동차 등록 현황", "FAQ"], label_visibility="collapsed")

# 메인 페이지 분기
if page == "자동차 등록 현황":
    show_ev_stats()
elif page == "FAQ":
    show_faq()
