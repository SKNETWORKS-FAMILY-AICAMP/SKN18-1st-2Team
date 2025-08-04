import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.db_utils import calculate_ev_ratio_data

# 페이지 설정
st.set_page_config(
    page_title="전기차 vs 일반차 비율 분석",
    layout="wide"
)

def load_data():
    """DB에서 데이터 로드"""
    try:
        df = calculate_ev_ratio_data()
        return df
    except Exception as e:
        st.error(f"데이터베이스에서 데이터를 불러올 수 없습니다: {str(e)}")
        return None

def main():
    # 커스텀 CSS 스타일
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .filter-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    .tab-content {
        padding: 2rem 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">전기차 vs 일반차 비율 분석</div>', unsafe_allow_html=True)
    
    # 데이터 로드
    df = load_data()
    if df is None:
        return
    
    # 사이드바 필터
    with st.sidebar:
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown("#### 필터 설정")
        
        # 연도 선택
        years = sorted(df['year'].unique())
        selected_years = st.multiselect(
            "연도 선택",
            options=years,
            default=years,
            help="분석할 연도를 선택하세요"
        )
        
        # 지역 선택
        regions = sorted(df['region'].unique())
        selected_regions = st.multiselect(
            "지역 선택",
            options=regions,
            default=regions,
            help="분석할 지역을 선택하세요"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 데이터 필터링
    filtered_df = df[
        (df['year'].isin(selected_years)) & 
        (df['region'].isin(selected_regions))
    ]
    
    if filtered_df.empty:
        st.warning("선택한 조건에 맞는 데이터가 없습니다.")
        return
    
    # 메인 지표 표시
    st.markdown("### 주요 지표")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_ev_ratio = filtered_df['ev_ratio'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_ev_ratio:.2f}%</div>
            <div class="metric-label">평균 전기차 비율</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        max_ev_ratio = filtered_df['ev_ratio'].max()
        max_region = filtered_df.loc[filtered_df['ev_ratio'].idxmax(), 'region']
        max_year = filtered_df.loc[filtered_df['ev_ratio'].idxmax(), 'year']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{max_ev_ratio:.2f}%</div>
            <div class="metric-label">최고 전기차 비율</div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem;">
                {max_year}년 {max_region}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # 최신 연도의 전기차 수만 합산 (누적 데이터이므로)
        latest_year = filtered_df['year'].max()
        latest_year_data = filtered_df[filtered_df['year'] == latest_year]
        total_ev = latest_year_data['electric_cars'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_ev:,}</div>
            <div class="metric-label">{latest_year}년 전기차 수</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # 최신 연도의 일반차 수만 합산 (누적 데이터이므로)
        total_general = latest_year_data['general_cars'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_general:,}</div>
            <div class="metric-label">{latest_year}년 일반차 수</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs(["연도별 추이", "지역별 비교", "상세 분석", "데이터 테이블"])
    
    with tab1:
        st.markdown('<div class="section-title">연도별 전기차 비율 추이</div>', unsafe_allow_html=True)
        
        # 연도별 평균 전기차 비율
        yearly_avg = filtered_df.groupby('year')['ev_ratio'].mean().reset_index()
        
        fig1 = px.line(
            yearly_avg, 
            x='year', 
            y='ev_ratio',
            title="연도별 평균 전기차 비율 추이",
            markers=True,
            labels={'ev_ratio': '전기차 비율 (%)', 'year': '연도'}
        )
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
        
        # 지역별 연도 추이 (선택한 상위 지역만)
        top_regions = filtered_df.groupby('region')['ev_ratio'].mean().nlargest(8).index
        top_df = filtered_df[filtered_df['region'].isin(top_regions)]
        
        fig2 = px.line(
            top_df,
            x='year',
            y='ev_ratio',
            color='region',
            title="주요 지역별 전기차 비율 추이 (상위 8개 지역)",
            markers=True,
            labels={'ev_ratio': '전기차 비율 (%)', 'year': '연도', 'region': '지역'}
        )
        fig2.update_layout(height=500)
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.markdown('<div class="section-title">지역별 전기차 비율 비교</div>', unsafe_allow_html=True)
        
        # 지역별 평균 전기차 비율
        region_avg = filtered_df.groupby('region')['ev_ratio'].mean().sort_values(ascending=True)
        
        fig3 = px.bar(
            x=region_avg.values,
            y=region_avg.index,
            orientation='h',
            title="지역별 평균 전기차 비율",
            labels={'x': '전기차 비율 (%)', 'y': '지역'},
            color=region_avg.values,
            color_continuous_scale='Viridis'
        )
        fig3.update_layout(height=600)
        st.plotly_chart(fig3, use_container_width=True)
        
        # 히트맵 - 연도별 지역별 전기차 비율
        pivot_df = filtered_df.pivot(index='region', columns='year', values='ev_ratio')
        
        fig4 = px.imshow(
            pivot_df,
            title="연도별 지역별 전기차 비율 히트맵",
            labels={'color': '전기차 비율 (%)'},
            color_continuous_scale='RdYlBu_r'
        )
        fig4.update_layout(height=600)
        st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        st.markdown('<div class="section-title">상세 분석</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 전기차 vs 일반차 비교 (최신년도)
            latest_year = filtered_df['year'].max()
            latest_df = filtered_df[filtered_df['year'] == latest_year]
            
            fig5 = px.scatter(
                latest_df,
                x='general_cars',
                y='electric_cars',
                color='ev_ratio',
                size='ev_ratio',
                hover_data=['region'],
                title=f"{latest_year}년 지역별 전기차 vs 일반차 등록수",
                labels={
                    'general_cars': '일반차 등록수',
                    'electric_cars': '전기차 등록수',
                    'ev_ratio': '전기차 비율 (%)'
                },
                color_continuous_scale='Viridis'
            )
            fig5.update_layout(height=400)
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            # 전기차 비율 분포
            fig6 = px.histogram(
                filtered_df,
                x='ev_ratio',
                nbins=20,
                title="전기차 비율 분포",
                labels={'ev_ratio': '전기차 비율 (%)', 'count': '빈도'}
            )
            fig6.update_layout(height=400)
            st.plotly_chart(fig6, use_container_width=True)
        
        # 상관관계 분석
        st.markdown('<div class="section-title">상관관계 분석</div>', unsafe_allow_html=True)
        corr_data = filtered_df[['general_cars', 'electric_cars', 'total_cars', 'ev_ratio']].corr()
        
        fig7 = px.imshow(
            corr_data,
            title="변수 간 상관관계",
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        fig7.update_layout(height=400)
        st.plotly_chart(fig7, use_container_width=True)
    
    with tab4:
        st.markdown('<div class="section-title">데이터 테이블</div>', unsafe_allow_html=True)
        
        # 정렬 옵션
        sort_options = {
            '연도 (오름차순)': ['year', True],
            '연도 (내림차순)': ['year', False],
            '전기차 비율 (높은순)': ['ev_ratio', False],
            '전기차 비율 (낮은순)': ['ev_ratio', True],
            '지역명 (가나다순)': ['region', True]
        }
        
        sort_choice = st.selectbox("정렬 기준", list(sort_options.keys()))
        sort_col, ascending = sort_options[sort_choice]
        
        # 데이터 정렬 및 표시
        display_df = filtered_df.sort_values(sort_col, ascending=ascending)
        
        # 컬럼명 한글화
        display_df_korean = display_df.copy()
        display_df_korean.columns = ['연도', '지역', '일반차수', '전기차수', '총차량수', '전기차비율(%)']
        
        st.dataframe(
            display_df_korean,
            use_container_width=True,
            hide_index=True
        )
        
        # 데이터 다운로드
        csv = display_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="데이터 다운로드 (CSV)",
            data=csv,
            file_name=f"ev_ratio_data_{'-'.join(map(str, selected_years))}.csv",
            mime="text/csv",
            type="primary"
        )
    
    # 푸터
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #f8fafc; padding: 2rem; border-radius: 12px; border: 1px solid #e2e8f0;">
        <h4 style="color: #374151; margin-bottom: 1rem;">데이터 정보</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; color: #6b7280;">
            <div>
                <strong>전기차 비율:</strong><br>
                전기차수 / (전기차수 + 일반차수) × 100
            </div>
            <div>
                <strong>기간:</strong><br>
                2020년 ~ 2024년 (5개년)
            </div>
            <div>
                <strong>지역:</strong><br>
                전국 17개 시도
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()