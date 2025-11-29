import streamlit as st
from calculator_logic import calculate # 이전 파일에서 만든 계산 로직 가져오기

# --- 페이지 설정 ---
st.set_page_config(page_title="Streamlit Button Calculator", layout="centered")
st.title("📱 버튼 기반 Streamlit 계산기")

# 세션 상태 초기화
if 'current_input' not in st.session_state:
    st.session_state.current_input = '0' # 현재 화면에 표시되는 값
if 'operator' not in st.session_state:
    st.session_state.operator = None     # 선택된 연산자
if 'first_number' not in st.session_state:
    st.session_state.first_number = None # 첫 번째 숫자 (피연산자)
if 'waiting_for_second' not in st.session_state:
    st.session_state.waiting_for_second = False # 두 번째 숫자 입력을 기다리는지 여부
if 'last_result' not in st.session_state:
    st.session_state.last_result = None # 마지막 계산 결과 (연속 계산용)

# --- 계산기 화면 출력 ---

# 결과 표시 창 (가장 크게)
st.markdown(
    f"<h1 style='text-align: right; margin-bottom: 0px;'>{st.session_state.current_input}</h1>", 
    unsafe_allow_html=True
)
st.markdown("---")
# --- 핵심 로직 함수 ---

def handle_number(number):
    """숫자 버튼 클릭 처리"""
    if st.session_state.waiting_for_second or st.session_state.current_input == '0' or st.session_state.last_result is not None:
        st.session_state.current_input = str(number)
        st.session_state.waiting_for_second = False
        st.session_state.last_result = None
    else:
        st.session_state.current_input += str(number)

def handle_decimal():
    """소수점 버튼 클릭 처리"""
    if '.' not in st.session_state.current_input:
        st.session_state.current_input += '.'

def handle_clear():
    """초기화 (AC) 버튼 클릭 처리"""
    st.session_state.current_input = '0'
    st.session_state.operator = None
    st.session_state.first_number = None
    st.session_state.waiting_for_second = False
    st.session_state.last_result = None

def handle_unary(op):
    """단항 연산 (sin, log 등) 처리"""
    try:
        num = float(st.session_state.current_input)
        # 로그의 밑은 10으로 고정 (간단한 계산기 모델)
        base = 10 if op == 'log' else None 
        
        result = calculate(num, None, op, base)
        
        if isinstance(result, str) and "Error" in result:
             st.session_state.current_input = result
        else:
            # 결과를 화면에 표시
            st.session_state.current_input = str(result)
            st.session_state.last_result = result
            
        st.session_state.waiting_for_second = True

    except ValueError:
        st.session_state.current_input = "Error: Invalid Input"

def handle_binary_operator(op):
    """이항 연산자 (+, -, *, / 등) 처리"""
    try:
        current_num = float(st.session_state.current_input)
        
        if st.session_state.first_number is None or st.session_state.last_result is not None:
            # 첫 연산이거나 마지막 결과 후 바로 연산자 누름
            st.session_state.first_number = current_num
            st.session_state.operator = op
            st.session_state.waiting_for_second = True
            st.session_state.last_result = None
        else:
            # 연속 연산: 이전 결과로 계산 후 새로운 연산자 저장
            result = calculate(st.session_state.first_number, current_num, st.session_state.operator)
            
            if isinstance(result, str) and "Error" in result:
                 st.session_state.current_input = result
                 handle_clear() # 에러 발생 시 초기화
            else:
                st.session_state.first_number = result
                st.session_state.operator = op
                st.session_state.current_input = str(result)
                st.session_state.waiting_for_second = True

    except ValueError:
        st.session_state.current_input = "Error: Invalid Input"

def handle_equals():
    """= 버튼 클릭 처리"""
    if st.session_state.operator and st.session_state.first_number is not None:
        try:
            second_num = float(st.session_state.current_input)
            
            result = calculate(st.session_state.first_number, second_num, st.session_state.operator)
            
            if isinstance(result, str) and "Error" in result:
                st.session_state.current_input = result
            else:
                # 결과 저장 및 상태 초기화
                st.session_state.current_input = str(result)
                st.session_state.first_number = None
                st.session_state.operator = None
                st.session_state.waiting_for_second = True # 다음 입력은 새 숫자
                st.session_state.last_result = result # 연속 계산을 위한 마지막 결과

        except ValueError:
            st.session_state.current_input = "Error: Invalid Input"

# --- 버튼 레이아웃 (5x5 그리드) ---
# 모든 버튼은 key를 명시적으로 지정해야 Streamlit이 제대로 추적합니다.

col_count = 5
cols = st.columns(col_count)

# 버튼 정의 (배열 형태로 정의하여 반복문으로 배치)
buttons = [
    # 1행: 특수 기능 및 클리어
    ('sin', lambda: handle_unary('sin'), cols[0]), 
    ('cos', lambda: handle_unary('cos'), cols[1]), 
    ('tan', lambda: handle_unary('tan'), cols[2]),
    ('log', lambda: handle_unary('log'), cols[3]), 
    ('AC', handle_clear, cols[4], {'type': 'primary'}), # AC 버튼 강조

    # 2행: 숫자 및 이항 연산자
    ('mod', lambda: handle_binary_operator('mod'), cols[0]),
    ('**', lambda: handle_binary_operator('**'), cols[1]),
    ('7', lambda: handle_number(7), cols[2]), 
    ('8', lambda: handle_number(8), cols[3]), 
    ('9', lambda: handle_number(9), cols[4]), 

    # 3행
    ('/', lambda: handle_binary_operator('/'), cols[0]),
    ('*', lambda: handle_binary_operator('*'), cols[1]),
    ('4', lambda: handle_number(4), cols[2]), 
    ('5', lambda: handle_number(5), cols[3]), 
    ('6', lambda: handle_number(6), cols[4]), 

    # 4행
    ('-', lambda: handle_binary_operator('-'), cols[0]),
    ('+', lambda: handle_binary_operator('+'), cols[1]),
    ('1', lambda: handle_number(1), cols[2]), 
    ('2', lambda: handle_number(2), cols[3]), 
    ('3', lambda: handle_number(3), cols[4]), 

    # 5행
    ('0', lambda: handle_number(0), cols[2]), # 0은 3열에 배치
    ('.', handle_decimal, cols[3]), 
    ('=', handle_equals, cols[4], {'type': 'primary'}), # = 버튼 강조
]

# 버튼 배치 루프
for label, callback, col, kwargs in buttons:
    with col:
        # style 인자 처리
        button_style = kwargs.get('type', 'secondary') 
        
        # 버튼 생성 및 콜백 함수 연결
        st.button(
            label, 
            on_click=callback, 
            key=f"btn_{label}", 
            use_container_width=True, # 버튼이 컬럼 폭에 꽉 차도록
            type=button_style
        )
        
st.markdown("---")
st.caption("사칙연산, Modulo, 지수, 로그(밑 10), 삼각함수(도 기준)를 지원합니다.")
