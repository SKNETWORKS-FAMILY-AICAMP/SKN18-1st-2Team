import streamlit as st
from db.data_process import do_process_data
from db.insert_ev_yearly_stats import insert_yearly_ev_data
from db.insert_kia_faq_data import insert_faq_data
from modules.kia_faq_action import main as faq_main
from modules.elec_car_action import main as elec_car_main

def crawl_faq():
    print("FAQ 크롤링 실행")
    with st.spinner("📦 FAQ 크롤링 중입니다..."):
        faq_main()
    st.success("✅ FAQ 크롤링 완료!")

def save_faq():
    print("FAQ 데이터 저장 실행")
    with st.spinner("💾 FAQ 저장 중입니다..."):
        insert_faq_data()
    st.success("✅ FAQ 저장 완료!")

def crawl_ev_data():
    print("전기차 데이터 크롤링 실행")
    with st.spinner("🚗 전기차 데이터 크롤링 중입니다..."):
        elec_car_main()
    st.success("✅ 전기차 데이터 크롤링 완료!")

def save_ev_data():
    print("전기차 데이터 전처리 및 저장 실행")
    with st.spinner("💽 전기차 데이터 전처리 중입니다..."):
        do_process_data()
    st.success("✅ 전기차 데이터 전치리 완료 -> 저장 시작!")
        
    with st.spinner("💽 전기차 데이터 저장 중입니다..."):
        insert_yearly_ev_data()
    st.success("✅ 전기차 데이터 저장 완료!")


def show_tool_page():
    st.write("🛠️ 필요한 데이터를 수집하고 저장합니다. 순서대로 실행하세요.")

    if st.button("FAQ 크롤링"):
        crawl_faq()
        
    if st.button("FAQ 데이터 저장"):
        save_faq()

    if st.button("전기차 데이터 크롤링"):
        crawl_ev_data()

    if st.button("전기차 데이터 저장"):
        save_ev_data()

    
