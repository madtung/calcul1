import streamlit as st
from calculator_logic import calculate 

# --- 페이지 설정 ---
st.set_page_config(page_title="Streamlit Button Calculator", layout="centered")
st.title("📱 버튼 기반 Streamlit 계산기")

# --- 1. 세션 상태 초기화 ---
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
st.markdown(
    f"<h1 style='text-align: right; margin-bottom: 0px;'>{st.session_state.current_input}</h1>", 
    unsafe_allow_html=True
)
st.markdown("---")

# --- 2. 핵심 로직 함수 (변경 없음) ---
# 이전 코드와 동일하므로 여기서는 생략하고, 파일에는 포함되어 있다고 가정합니다.

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
        base = 10 if op == 'log' else None 
        result = calculate(num, None, op, base)
        
        if isinstance(result, str) and "Error" in result:
             st.session_state.current_input = result
        else:
            if isinstance(result, (int, float)):
                st.session_state.current_input = f"{result:.10g}" if abs(result) < 1e10 else str(result)
            else:
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
            st.session_state.first_number = current_num
            st.session_state.operator = op
            st.session_state.waiting_for_second = True
            st.session_state.last_result = None
        else:
            result = calculate(st.session_state.first_number, current_num, st.session_state.operator)
            
            if isinstance(result, str) and "Error" in result:
                 st.session_state.current_input = result
                 st.session_state.first_number = None
                 st.session_state.operator = None
                 st.session_state.waiting_for_second = True
            else:
                st.session_state.first_number = result
                st.session_state.operator = op
                st.session_state.current_input = f"{result:.10g}"
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
                if isinstance(result, (int, float)):
                    st.session_state.current_input = f"{result:.10g}"
                else:
                    st.session_state.current_input = str(result)
                
                st.session_state.first_number = None
                st.session_state.operator = None
                st.session_state.waiting_for_second = True
                st.session_state.last_result = result

        except ValueError:
            st.session_state.current_input = "Error: Invalid Input"

# (앞부분의 import, session_state 초기화, 함수 정의는 그대로 둡니다.)
# ...

# --- 3. 버튼 레이아웃 및 연결 (수정된 부분) ---

col_count = 5
cols = st.columns(col_count)

# 버튼 정의 함수 매핑 (레이블은 길어졌지만, 콜백은 기존 연산자를 사용합니다.)
button_map = {
    'sin': lambda: handle_unary('sin'), 'cos': lambda: handle_unary('cos'), 'tan': lambda: handle_unary('tan'), 'log': lambda: handle_unary('log'), 
    'AC': handle_clear, 'mod': lambda: handle_binary_operator('mod'), 'EXP': lambda: handle_binary_operator('**'), # ** -> EXP
    '7': lambda: handle_number(7), '8': lambda: handle_number(8), '9': lambda: handle_number(9),
    'DIV': lambda: handle_binary_operator('/'), 'MUL': lambda: handle_binary_operator('*'), # / -> DIV, * -> MUL
    '4': lambda: handle_number(4), '5': lambda: handle_number(5), '6': lambda: handle_number(6),
    'SUB': lambda: handle_binary_operator('-'), 'ADD': lambda: handle_binary_operator('+'), # - -> SUB, + -> ADD
    '1': lambda: handle_number(1), '2': lambda: handle_number(2), '3': lambda: handle_number(3),
    '0': lambda: handle_number(0), '.': handle_decimal, '=': handle_equals,
    '': lambda: None # 공백 버튼용 콜백
}

# 최종 버튼 배치 그리드 (레이블 변경 적용)
calculator_grid = [
    # C0, C1, C2, C3, C4
    ['sin', 'cos', 'tan', 'log', 'AC'],
    ['mod', 'EXP', '7', '8', '9'],
    ['DIV', 'MUL', '4', '5', '6'],
    ['SUB', 'ADD', '1', '2', '3'], # 뺄셈(SUB), 덧셈(ADD) 사용
    ['', '', '0', '.', '='], 
]

# 최종 버튼 배치 루프
for row_labels in calculator_grid:
    cols = st.columns(5)
    for i, label in enumerate(row_labels):
        callback = button_map[label]
        
        # AC와 = 버튼에만 'primary' 스타일 적용
        button_type = 'primary' if label in ['AC', '='] else 'secondary'
        
        with cols[i]:
            button_label = label if label != '' else ' '
            
            st.button(
                button_label, 
                on_click=callback, 
                key=f"btn_{label}_{i}", 
                use_container_width=True, 
                type=button_type
            )
        
st.markdown("---")
st.caption("사칙연산 버튼 레이블을 영어 약자(ADD, SUB, MUL, DIV)로 변경하여 표시 오류를 해결했습니다.")


import streamlit as st
from calculator_page import calculator_page, init_calculator_state
from probability_page import probability_page
from world_population_page import world_population_page # 새 페이지 임포트

# --- 1. 페이지 설정 및 라우팅 ---
st.set_page_config(
    page_title="통합 웹 앱 (다기능)",
    layout="wide" # 지도 시각화를 위해 레이아웃을 'wide'로 변경
)

# 사이드바에서 페이지 선택
st.sidebar.title("메인 메뉴")
page = st.sidebar.radio(
    "원하는 앱을 선택하세요:",
    ["계산기 📱", "확률 시뮬레이터 🎲", "연도별 세계 인구 분석 🌍"]
)

st.title(f"통합 웹 앱: {page}")
st.markdown("---")

# --- 2. 페이지별 분기 처리 및 함수 호출 ---

if page == "계산기 📱":
    init_calculator_state()
    st.header("고급 버튼 계산기")
    # 계산기 UI는 'centered' 레이아웃이 더 적합하지만, 전체 앱은 'wide'를 따릅니다.
    calculator_page() 
    
elif page == "확률 시뮬레이터 🎲":
    probability_page()

elif page == "연도별 세계 인구 분석 🌍":
    world_population_page()

# --- app.py 끝 ---
