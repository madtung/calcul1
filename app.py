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


# --- 3. 버튼 레이아웃 및 연결 (수정된 부분) ---

col_count = 5
cols = st.columns(col_count)

# 버튼 정의 (수정된 배치)
buttons_data = [
    # 1행: 특수 기능 및 클리어
    ('sin', lambda: handle_unary('sin'), cols[0]), 
    ('cos', lambda: handle_unary('cos'), cols[1]), 
    ('tan', lambda: handle_unary('tan'), cols[2]),
    ('log', lambda: handle_unary('log'), cols[3]), 
    ('AC', handle_clear, cols[4], {'type': 'primary'}), # AC 버튼 강조

    # 2행: Mod, 지수, 7, 8, 9
    ('mod', lambda: handle_binary_operator('mod'), cols[0]),
    ('**', lambda: handle_binary_operator('**'), cols[1]),
    ('7', lambda: handle_number(7), cols[2]), 
    ('8', lambda: handle_number(8), cols[3]), 
    ('9', lambda: handle_number(9), cols[4]), 

    # 3행: 나눗셈(/), 곱셈(*), 4, 5, 6
    ('/', lambda: handle_binary_operator('/'), cols[0]),
    ('*', lambda: handle_binary_operator('*'), cols[1]),
    ('4', lambda: handle_number(4), cols[2]), 
    ('5', lambda: handle_number(5), cols[3]), 
    ('6', lambda: handle_number(6), cols[4]), 

    # 4행: 뺄셈(-), 덧셈(+), 1, 2, 3
    ('-', lambda: handle_binary_operator('-'), cols[0]),
    ('+', lambda: handle_binary_operator('+'), cols[1]),
    ('1', lambda: handle_number(1), cols[2]), 
    ('2', lambda: handle_number(2), cols[3]), 
    ('3', lambda: handle_number(4), cols[4]), # <-- 오류 수정: 3행 5열은 3을 가져야 함

    # 5행: 공백, 공백, 0, 소수점(.), 이퀄(=)
    ('', lambda: None, cols[0]), # 공백 버튼 (cols[0])
    ('', lambda: None, cols[1]), # 공백 버튼 (cols[1])
    ('0', lambda: handle_number(0), cols[2]), 
    ('.', handle_decimal, cols[3]), 
    ('=', handle_equals, cols[4], {'type': 'primary'}), # = 버튼 강조
]

# 버튼 정의 (배치 오류 수정된 버전)
buttons_data = [
    # 1행
    ('sin', lambda: handle_unary('sin'), cols[0]), ('cos', lambda: handle_unary('cos'), cols[1]), 
    ('tan', lambda: handle_unary('tan'), cols[2]), ('log', lambda: handle_unary('log'), cols[3]), 
    ('AC', handle_clear, cols[4], {'type': 'primary'}), 

    # 2행
    ('mod', lambda: handle_binary_operator('mod'), cols[0]), ('**', lambda: handle_binary_operator('**'), cols[1]), 
    ('7', lambda: handle_number(7), cols[2]), ('8', lambda: handle_number(8), cols[3]), 
    ('9', lambda: handle_number(9), cols[4]), 

    # 3행
    ('/', lambda: handle_binary_operator('/'), cols[0]), ('*', lambda: handle_binary_operator('*'), cols[1]), 
    ('4', lambda: handle_number(4), cols[2]), ('5', lambda: handle_number(5), cols[3]), 
    ('6', lambda: handle_number(6), cols[4]), 

    # 4행 (사칙연산 버튼을 4열에 위치시키고 숫자 버튼은 3열에)
    ('1', lambda: handle_number(1), cols[2]), ('2', lambda: handle_number(2), cols[3]), 
    ('3', lambda: handle_number(3), cols[4]), 
    ('-', lambda: handle_binary_operator('-'), cols[0]), # 뺄셈을 왼쪽 끝으로 이동
    ('+', lambda: handle_binary_operator('+'), cols[1]), # 덧셈을 그 옆으로 이동

    # 5행
    ('0', lambda: handle_number(0), cols[2]), ('.', handle_decimal, cols[3]), 
    ('=', handle_equals, cols[4], {'type': 'primary'}), 
]


# 버튼 배치 루프 (수정된 4, 5행의 버튼 배열 순서를 반영)
# 버튼 배치를 그리드에 맞추어 재구성합니다. 5열 계산기 디자인에 맞게 순서를 조정했습니다.
calculator_grid = [
    # C0, C1, C2, C3, C4
    ['sin', 'cos', 'tan', 'log', 'AC'],
    ['mod', '**', '7', '8', '9'],
    ['/', '*', '4', '5', '6'],
    ['-', '+', '1', '2', '3'], # 뺄셈, 덧셈을 1, 2열에 배치
    ['', '', '0', '.', '='], 
]

# 버튼 정의 함수 매핑
button_map = {
    'sin': lambda: handle_unary('sin'), 'cos': lambda: handle_unary('cos'), 'tan': lambda: handle_unary('tan'), 'log': lambda: handle_unary('log'), 
    'AC': handle_clear, 'mod': lambda: handle_binary_operator('mod'), '**': lambda: handle_binary_operator('**'),
    '7': lambda: handle_number(7), '8': lambda: handle_number(8), '9': lambda: handle_number(9),
    '/': lambda: handle_binary_operator('/'), '*': lambda: handle_binary_operator('*'), 
    '4': lambda: handle_number(4), '5': lambda: handle_number(5), '6': lambda: handle_number(6),
    '-': lambda: handle_binary_operator('-'), '+': lambda: handle_binary_operator('+'), 
    '1': lambda: handle_number(1), '2': lambda: handle_number(2), '3': lambda: handle_number(3),
    '0': lambda: handle_number(0), '.': handle_decimal, '=': handle_equals,
    '': lambda: None # 공백 버튼용 콜백
}

# 최종 버튼 배치 루프
for row_labels in calculator_grid:
    # 5개의 컬럼을 한 행으로 설정
    cols = st.columns(5)
    for i, label in enumerate(row_labels):
        callback = button_map[label]
        
        # AC와 = 버튼에만 'primary' 스타일 적용
        button_type = 'primary' if label in ['AC', '='] else 'secondary'
        
        with cols[i]:
            # 공백 버튼일 경우 빈 문자열 표시
            button_label = label if label != '' else ' '
            
            st.button(
                button_label, 
                on_click=callback, 
                key=f"btn_{label}_{i}", 
                use_container_width=True, 
                type=button_type
            )
        
st.markdown("---")
st.caption("사칙연산, Modulo, 지수, 로그(밑 10), 삼각함수(도 기준)를 지원합니다. 버튼 레이아웃을 계산기 모양에 맞게 수정했습니다.")
