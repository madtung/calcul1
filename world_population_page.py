import streamlit as st
import pandas as pd
import plotly.express as px
import os # 파일 경로 관리를 위해 os 모듈 추가

# 🚨 로컬 파일 경로 설정
# world_population.csv 파일이 app.py 및 world_population_page.py와 같은 디렉토리에 있다고 가정합니다.
CSV_FILE_PATH = "world_population.csv"

# 캐시 키를 파일 이름과 크기로 설정하여, 파일이 변경되면 자동으로 다시 로드하도록 설정합니다.
@st.cache_data
def load_data(file_path):
    """로컬 CSV 파일을 로드하고 캐싱합니다."""
    try:
        # 파일이 존재하는지 확인
        if not os.path.exists(file_path):
            st.error(f"파일을 찾을 수 없습니다: {file_path}. 해당 파일이 앱 폴더에 있는지 확인해 주세요.")
            return pd.DataFrame() 
            
        df = pd.read_csv(file_path)
        # 데이터프레임의 컬럼 이름을 모두 소문자로 변경하여 접근을 쉽게 합니다.
        df.columns = df.columns.str.lower()
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다. CSV 파일의 형식이나 인코딩을 확인하세요: {e}")
        return pd.DataFrame() # 빈 데이터프레임 반환

def world_population_page():
    """연도별 세계 인구 분석 페이지 UI를 렌더링합니다."""
    st.header("🌍 연도별 세계 인구 분석 (world_population.csv 사용)")
    st.markdown("---")

    # CSV 데이터 로드
    df_raw = load_data(CSV_FILE_PATH)

    if df_raw.empty:
        # 데이터 로드에 실패하면 메시지를 표시하고 종료
        st.warning("데이터 파일을 로드할 수 없습니다. 파일을 확인해 주세요.")
        return
    
    # --- 데이터 전처리 및 연도 선택 ---
    
    # CSV 파일이 다음 컬럼들을 포함한다고 가정합니다: 'year', 'iso_a3', 'population'
    try:
        # 연도 목록 추출
        POPULATION_YEARS = sorted(df_raw['year'].unique())
        if 'population' not in df_raw.columns:
             st.error("CSV 파일에 'population' 컬럼이 없습니다. 파일의 컬럼 이름을 확인해 주세요.")
             return
    except KeyError as e:
        st.error(f"CSV 파일에 필요한 컬럼이 없습니다: {e}. 'year', 'iso_a3', 'population' 컬럼 이름을 확인해 주세요.")
        return

    # 1. 연도 선택 드롭다운 박스
    selected_year = st.selectbox(
        "분석할 연도를 선택하세요:",
        options=POPULATION_YEARS,
        index=len(POPULATION_YEARS) - 1,
        key="pop_year_select"
    )

    # 2. 선택된 연도 데이터 필터링
    df = df_raw[df_raw['year'] == selected_year].copy()
    
    # 3. 인구 구간별 색상 설정 및 시각화 (Choropleth 맵 생성)
    
    color_scale = "Viridis" 

    fig = px.choropleth(
        df,
        locations='iso_a3',           # CSV 파일의 국가 코드 컬럼 (ISO-3)
        color='population',           # 색상 구분에 사용할 값 (인구)
        hover_name='iso_a3',          
        color_continuous_scale=color_scale, 
        title=f"{selected_year}년 국가별 인구 분포",
        projection="natural earth"
    )

    # 색상 바의 범례 설정
    pop_min = df['population'].min()
    pop_median = df['population'].median()
    pop_max = df['population'].max()
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="인구 수",
            tickvals=[pop_min, pop_median, pop_max],
            ticktext=[
                f"{pop_min:,.0f} (최소)", 
                f"{pop_median:,.0f} (중간값)", 
                f"{pop_max:,.0f} (최대)"
            ]
        )
    )

    # Streamlit에 Plotly 지도 표시
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("선택된 데이터 미리보기")
    st.dataframe(df)
