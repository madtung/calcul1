import streamlit as st
# calculator_logic.py는 같은 디렉토리에 있다고 가정합니다.
from calculator_logic import calculate 

def init_calculator_state():
    """계산기 전용 세션 상태를 초기화합니다."""
    if 'current_input' not in st.session_state:
        st.session_state.current_input = '0'
    if 'operator' not in st.session_state:
        st.session_state.operator = None
    if 'first_number' not in st.session_state:
        st.session_state.first_number = None
    if 'waiting_for_second' not in st.session_state:
        st.session_state.waiting_for_second = False
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None

# --- 핵심 로직 함수 (이전 app.py에서 사용한 함수 그대로 사용) ---

def handle_number(number):
    if st.session_state.waiting_for_second or st.session_state.current_input == '0' or st.session_state.last_result is not None:
        st.session_state.current_input = str(number)
        st.session_state.waiting_for_second = False
        st.session_state.last_result = None
    else:
        st.session_state.current_input += str(number)

def handle_decimal():
    if '.' not in st.session_state.current_input:
        st.session_state.current_input += '.'

def handle_clear():
    st.session_state.current_input = '0'
    st.session_state.operator = None
    st.session_state.first_number = None
    st.session_state.waiting_for_second = False
    st.session_state.last_result = None

def handle_unary(op):
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

# --- 메인 계산기 페이지 함수 ---

def calculator_page():
    """계산기 페이지 UI를 렌더링합니다."""
    st.markdown(
        f"<h1 style='text-align: right; margin-bottom: 0px;'>{st.session_state.current_input}</h1>", 
        unsafe_allow_html=True
    )
    st.markdown("---")

    col_count = 5
    # 버튼 매핑
    button_map = {
        'sin': lambda: handle_unary('sin'), 'cos': lambda: handle_unary('cos'), 'tan': lambda: handle_unary('tan'), 'log': lambda: handle_unary('log'), 
        'AC': handle_clear, 'mod': lambda: handle_binary_operator('mod'), 'EXP': lambda: handle_binary_operator('**'),
        '7': lambda: handle_number(7), '8': lambda: handle_number(8), '9': lambda: handle_number(9),
        'DIV': lambda: handle_binary_operator('/'), 'MUL': lambda: handle_binary_operator('*'), 
        '4': lambda: handle_number(4), '5': lambda: handle_number(5), '6': lambda: handle_number(6),
        'SUB': lambda: handle_binary_operator('-'), 'ADD': lambda: handle_binary_operator('+'), 
        '1': lambda: handle_number(1), '2': lambda: handle_number(2), '3': lambda: handle_number(3),
        '0': lambda: handle_number(0), '.': handle_decimal, '=': handle_equals,
        '': lambda: None
    }

    # 버튼 배치 그리드
    calculator_grid = [
        ['sin', 'cos', 'tan', 'log', 'AC'],
        ['mod', 'EXP', '7', '8', '9'],
        ['DIV', 'MUL', '4', '5', '6'],
        ['SUB', 'ADD', '1', '2', '3'], 
        ['', '', '0', '.', '='], 
    ]

    # 최종 버튼 배치 루프
    for row_labels in calculator_grid:
        cols = st.columns(5)
        for i, label in enumerate(row_labels):
            callback = button_map[label]
            button_type = 'primary' if label in ['AC', '='] else 'secondary'
            
            with cols[i]:
                button_label = label if label != '' else ' '
                
                st.button(
                    button_label, 
                    on_click=callback, 
                    key=f"calc_btn_{label}_{i}",  # 키 충돌 방지를 위해 접두사 추가
                    use_container_width=True, 
                    type=button_type
                )
            
    st.markdown("---")
    st.caption("고급 계산기: ADD, SUB, MUL, DIV, Mod, 지수, 로그(밑 10), 삼각함수(도 기준) 지원.")

# --- calculator_page.py 끝 ---
