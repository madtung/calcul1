import numpy as np
import cmath # 복소수 계산을 위해 cmath 모듈을 가져옵니다.

def calculate(num1, num2, operation, base=None):
    """
    주어진 두 숫자와 연산자에 따라 계산을 수행합니다.
    """
    try:
        # 1. 사칙연산, Modulo, 지수 (Exponentiation)
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 == 0:
                return "Error: Division by zero"
            return num1 / num2
        elif operation == 'mod':
            if num2 == 0:
                return "Error: Modulo by zero"
            return num1 % num2
        elif operation == '**': # 지수
            return num1 ** num2

        # 2. 로그 연산 (num2는 무시)
        elif operation == 'log':
            if num1 <= 0:
                return "Error: Log domain error (x <= 0)"
            # base가 주어지지 않으면 자연로그(ln)
            if base is None or base == 0:
                return np.log(num1) # 자연로그 (ln)
            elif base > 0 and base != 1:
                return np.log(num1) / np.log(base) # 로그 밑변환 공식
            else:
                return "Error: Invalid log base"

        # 3. 삼각함수 (num2는 무시)
        # NumPy 함수는 인수를 '라디안'으로 가정합니다.
        elif operation == 'sin':
            return np.sin(np.radians(num1)) # 각도를 라디안으로 변환
        elif operation == 'cos':
            return np.cos(np.radians(num1))
        elif operation == 'tan':
            # 90도와 그 홀수 배수 근처에서 오류를 처리할 수 있습니다.
            if np.isclose(np.cos(np.radians(num1 % 180)), 0):
                 return "Error: Tangent undefined"
            return np.tan(np.radians(num1))
        
        else:
            return "Error: Invalid operation"
            
    except Exception as e:
        return f"Calculation Error: {e}"
