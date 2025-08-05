import streamlit as st
from db.data_process import do_process_data
from db.excel_to_csv_converter import process_excel_to_csv
from db.insert_car_csv_data import insert_car_data_from_csv
from db.insert_ev_brand_stats import insert_ev_brand
from db.insert_ev_region_stats import insert_ev_region
from db.insert_ev_yearly_stats import insert_yearly_ev_data
from db.insert_kia_faq_data import insert_faq_data
from db.insert_veh_fuel_stats import insert_veh_fuel
from modules.kia_faq_action import main as faq_main
from modules.elec_car_action import main as elec_car_main
from modules.crawl_car_data import main as crawl_car_main  


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
    
def save_fuel_data():
    print("연료별 데이터 저장 실행")
    with st.spinner("💽 연료별 데이터 brand 중입니다..."):
        insert_ev_brand()
    st.success("✅ 연료별 데이터 brand 저장 완료")
        
    with st.spinner("💽 연료별 데이터 region 중입니다..."):
        insert_ev_region()
    st.success("✅ 연료별 데이터 region 저장 완료")
    
    with st.spinner("💽 연료별 데이터 fuel 중입니다..."):
        insert_veh_fuel()
    st.success("✅ 연료별 데이터 fuel 저장 완료")
    
    
def crawl_allcar_data():
    print("자동차등록현황보고 크롤링")
    with st.spinner("🚗 자동차등록현황보고 크롤링 중입니다..."):
        crawl_car_main()
    st.success("✅ 자동차등록현황보고 크롤링 완료!")

def convert_allcar_data():
    print("자동차등록현황보고 전처리")
    with st.spinner("🚗 자동차등록현황보고 전처리 중입니다..."):
        process_excel_to_csv()
    st.success("✅ 자동차등록현황보고 전처리 완료!")
    
def save_allcar_data():
    print("자동차등록현황보고 저장")
    with st.spinner("🚗 자동차등록현황보고 저장 중입니다..."):
        print("CSV에서 자동차 등록 통계 데이터 삽입 시작...")
        insert_car_data_from_csv()
        print("완료!")
    st.success("✅ 자동차등록현황보고 저장 완료!")

## SHOW PAGE
def show_tool_page():
    st.write("🛠️ 필요한 데이터를 수집하고 저장합니다. 순서대로 실행하세요.")
    st.write("** db/create_tables.sql 실행 **")

    if st.button("FAQ 크롤링"):
        crawl_faq()
        
    if st.button("FAQ 데이터 저장"):
        save_faq()

    if st.button("전기차 데이터 크롤링"):
        crawl_ev_data()

    if st.button("전기차 데이터 저장"):
        save_ev_data()
        
    if st.button("연료 관련 데이터 저장"):
        save_fuel_data()
        
    if st.button("자동차등록현황보고 크롤링"):
        crawl_allcar_data()

    if st.button("자동차등록현황보고 전처리"):
        convert_allcar_data()
    
    if st.button("자동차등록현황보고 저장"):
        save_allcar_data()
    

    
