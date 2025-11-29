import streamlit as st
from calculator_logic import calculate
import numpy as np

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Advanced Streamlit Calculator",
    layout="centered"
)

st.title("🔢 고급 Streamlit 계산기")

# --- 연산자 및 입력 설정 ---

# 연산자 목록 (사칙연산, mod, 지수, 특수 연산)
binary_operations = {
    '+': '덧셈 (Add)', '-': '뺄셈 (Subtract)', '*': '곱셈 (Multiply)', 
    '/': '나눗셈 (Divide)', 'mod': '나머지 (Modulo)', '**': '지수 (Power)'
}

# 단일 숫자 입력이 필요한 연산자 목록 (로그, 삼각함수)
unary_operations = {
    'log': '로그 (Log)', 'sin': '사인 (Sine)', 'cos': '코사인 (Cosine)', 'tan': '탄젠트 (Tangent)'
}

# 탭을 사용하여 입력 UI를 분리
tab_binary, tab_unary = st.tabs(["이항 연산 (Binary Ops)", "단항 연산 (Unary Ops)"])

with tab_binary:
    st.header("두 숫자를 사용하는 연산")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 사용자 입력: 숫자 1
        num1_bin = st.number_input("첫 번째 숫자 (Num1)", value=0.0, format="%.5f", key="n1_bin")
    
    with col2:
        # 사용자 입력: 연산자 선택
        operation_bin_label = st.selectbox(
            "연산 선택", 
            options=list(binary_operations.keys()), 
            format_func=lambda x: binary_operations[x], 
            key="op_bin"
        )
    
    # 숫자 2 입력
    num2_bin = st.number_input("두 번째 숫자 (Num2)", value=0.0, format="%.5f", key="n2_bin")

    
    # 계산 버튼
    if st.button("계산 실행 (Binary)", key="calc_bin"):
        # 계산 함수 호출
        result_bin = calculate(num1_bin, num2_bin, operation_bin_label)
        
        # 결과 표시
        st.success(f"**결과:** {result_bin}")
        
    st.markdown("---")
    st.caption("*참고: 모든 입력은 실수(Float)로 처리됩니다.*")


with tab_unary:
    st.header("하나의 숫자를 사용하는 연산 (Num1)")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # 사용자 입력: 숫자 1
        num1_uni = st.number_input("숫자 (Num1)", value=0.0, format="%.5f", key="n1_uni")
    
    with col4:
        # 사용자 입력: 단항 연산자 선택
        operation_uni_label = st.selectbox(
            "연산 선택", 
            options=list(unary_operations.keys()), 
            format_func=lambda x: unary_operations[x], 
            key="op_uni"
        )
        
    # 로그의 밑(Base) 입력 (로그 연산일 경우에만 표시)
    log_base = None
    if operation_uni_label == 'log':
        log_base = st.number_input("로그의 밑 (Base, 0 입력 시 자연로그(ln))", value=0.0, format="%.5f", key="log_base")
        st.caption("**:red[삼각함수]** 연산 시, 입력값은 **도(degree)**로 간주됩니다.")


    # 계산 버튼
    if st.button("계산 실행 (Unary)", key="calc_uni"):
        if operation_uni_label == 'log':
             # 로그 연산일 경우, calculate 함수에 밑(base)을 전달
             result_uni = calculate(num1_uni, None, operation_uni_label, base=log_base)
        else:
             # 기타 단항 연산일 경우 (num2는 None으로 설정)
             result_uni = calculate(num1_uni, None, operation_uni_label)
        
        # 결과 표시
        st.success(f"**결과:** {result_uni}")
        
    st.markdown("---")
    # LaTeX를 사용하여 삼각함수 설명
    st.markdown("### 주요 수학 상수")
    st.latex(r'''
        \pi \approx 3.14159... \\
        e \approx 2.71828...
    ''')
    st.caption("NumPy를 사용하여 계산합니다.")
