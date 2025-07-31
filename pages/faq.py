import streamlit as st
import pandas as pd
from db.db_utils import get_conn

def show_faq():
    st.markdown("<h1 style='font-weight:bold;'>KIA FAQ</h1>", unsafe_allow_html=True)
    st.write("궁금하신 내용은 검색을 통해 더 편리하게 확인할 수 있습니다.")

    # DB에서 불러오기
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM kia_faq_data", conn)
    conn.close()

    # 카테고리 목록
    categories = ["전체"] + sorted(df["category"].dropna().unique().tolist())
    selected_category = st.selectbox("카테고리 선택", categories)

    # 질문 검색창
    search_query = st.text_input("질문 검색", "")

    # 필터링
    filtered_df = df.copy()
    if selected_category != "전체":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    if search_query:
        filtered_df = filtered_df[filtered_df["question"].str.contains(search_query, case=False, na=False)]

    # 질문 리스트 아코디언
    for idx, row in filtered_df.iterrows():
        with st.expander("Q. " + row["question"]):
            st.markdown("**A. " + row["answer_text"] + "**")
            if row["image_urls"]:
                for img_url in str(row["image_urls"]).split(","):
                    if img_url.strip().startswith("http"):
                        st.image(img_url.strip())
            if row["link_urls"]:
                for link_url in str(row["link_urls"]).split(","):
                    if link_url.strip().startswith("http"):
                        st.markdown(f"[관련 링크]({link_url.strip()})", unsafe_allow_html=True)
