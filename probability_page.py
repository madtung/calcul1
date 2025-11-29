import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

def probability_page():
    """확률 시뮬레이터 페이지 UI를 렌더링합니다."""
    st.header("🎲 확률 시뮬레이터")
    
    # --- 1. 입력 설정 ---
    col1, col2 = st.columns(2)
    
    with col1:
        simulation_type = st.selectbox(
            "시뮬레이션 선택",
            options=["주사위 던지기 (Dice)", "동전 던지기 (Coin)"],
            key="sim_type"
        )
        
    with col2:
        num_trials = st.number_input(
            "실행 횟수 (시행 횟수)",
            min_value=1,
            max_value=100000,
            value=1000,
            step=100,
            key="num_trials"
        )
        
    st.markdown("---")
    
    # --- 2. 시뮬레이션 및 결과 계산 ---
    
    if st.button("시뮬레이션 실행", key="run_sim"):
        
        # 결과 저장 딕셔너리
        results = {}
        
        if simulation_type == "주사위 던지기 (Dice)":
            # 1~6 사이의 정수 난수 생성
            rolls = np.random.randint(1, 7, size=num_trials)
            st.subheader("주사위 던지기 결과")
            # 결과 집계 (1, 2, 3, 4, 5, 6)
            for i in range(1, 7):
                results[str(i)] = np.sum(rolls == i)
            
            # 이론적 확률과 비교
            expected_prob = 1 / 6
            st.info(f"이론적 확률 (각 면): {expected_prob:.4f} (약 16.67%)")
            
        else: # 동전 던지기 (Coin)
            # 0 (뒷면) 또는 1 (앞면) 난수 생성
            flips = np.random.randint(0, 2, size=num_trials)
            st.subheader("동전 던지기 결과")
            # 결과 집계 (앞면, 뒷면)
            results["앞면 (Head)"] = np.sum(flips == 1)
            results["뒷면 (Tail)"] = np.sum(flips == 0)

            # 이론적 확률과 비교
            expected_prob = 0.5
            st.info(f"이론적 확률 (각 면): {expected_prob:.4f} (50%)")

        # --- 3. Plotly 시각화 ---
        
        # 데이터프레임 생성
        df = pd.DataFrame(results.items(), columns=['결과', '횟수'])
        df['빈도 (%)'] = (df['횟수'] / num_trials) * 100
        
        # Plotly 막대 그래프 생성
        fig = px.bar(
            df, 
            x='결과', 
            y='빈도 (%)', 
            text='횟수',
            title=f"총 {num_trials}회 시뮬레이션 결과",
            labels={'결과': '결과', '빈도 (%)': '빈도 (%)', '횟수': '발생 횟수'},
            color='결과'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis={'categoryorder':'total ascending'})
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df)

# --- probability_page.py 끝 ---
