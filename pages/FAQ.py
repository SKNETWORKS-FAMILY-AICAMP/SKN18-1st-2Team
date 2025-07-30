import streamlit as st

# ---------------------------------------
# ✅ 타이틀 + 안내 문구
# ---------------------------------------
st.markdown("<h1 style='text-align: center;'>FAQ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>궁금하신 내용을 검색을 통해 좀 더 편리하게 확인할 수 있습니다.</p>", unsafe_allow_html=True)

# ---------------------------------------
# ✅ 검색창 + 버튼 (가운데 정렬)
# ---------------------------------------
col_center = st.columns([1, 5, 1])

with col_center[1]:
    input_col, button_col = st.columns([6, 1])

    with input_col:
        search_input = st.text_input("검색", placeholder="🔍 검색어를 입력하세요", label_visibility="collapsed")

    with button_col:
        search = st.button("검색")

# ---------------------------------------
# ✅ 샘플 FAQ 데이터 (카테고리별 질문만, 답변은 나중에)
# ---------------------------------------
faq_data = [
    {"category": "차량 구매", "question": "질문1", "answer": "답변은 준비 중입니다."},
    {"category": "차량 구매", "question": "질문2", "answer": "답변은 준비 중입니다."},
    {"category": "기아멤버스", "question": "질문1", "answer": "답변은 준비 중입니다."},
    {"category": "기아멤버스", "question": "질문2", "answer": "답변은 준비 중입니다."},
    {"category": "TOP10", "question": "질문1", "answer": "답변은 준비 중입니다."},
    {"category": "TOP10", "question": "질문2", "answer": "답변은 준비 중입니다."},
    {"category": "차량 정비", "question": "질문1", "answer": "답변은 준비 중입니다."},
    {"category": "홈페이지", "question": "질문1", "answer": "답변은 준비 중입니다."},
    {"category": "PBV", "question": "질문1", "answer": "답변은 준비 중입니다."},
    {"category": "기타", "question": "질문1", "answer": "답변은 준비 중입니다."},
]

# ---------------------------------------
# ✅ 카테고리 탭 구성
# ---------------------------------------
tab_names = ["TOP10", "전체", "차량 구매", "차량 정비", "기아멤버스", "홈페이지", "PBV", "기타"]
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        selected_category = tab_names[i]

        # 검색 시 필터링
        if search and search_input:
            filtered_faqs = [item for item in faq_data if search_input.lower() in item["question"].lower()]
            st.markdown(f"🔍 검색어 '{search_input}'에 대한 결과입니다:")
        else:
            # 카테고리 필터링
            if selected_category == "전체":
                filtered_faqs = faq_data
            else:
                filtered_faqs = [item for item in faq_data if item["category"] == selected_category]

        # 질문 출력
        if filtered_faqs:
            for faq in filtered_faqs:
                with st.expander(faq["question"]):
                    st.write(faq["answer"])
        else:
            st.info("해당 카테고리에 등록된 질문이 없습니다.")
