#-*- coding: utf-8 -*-
import datetime, types, functools

#출처 : https://velog.io/@doondoony/Python-Decorator-101
# JAVA 의 annotation 과는 근원적으로 다르다. > 파이썬의 데코레이터는 단순히 함수를 실행 하기 전에 지정된 클래스의 함수 또는 함수에 실행 함수를 전달 하는 것뿐이기 때문이다.

# 데코레이터는 클로저라고 표현하며 풀어서는 클로저의 축약 문법이라고 나타낸다.

# 1. 같은 기능을 가진코드가 반복 되는 유형

def calc_add(a: int, b: int):
    _IS_DEBUG = True 
    if _IS_DEBUG: print("-------calc_add-------start")
    result = a + b
    if _IS_DEBUG: 
        print("-------calc_add-------end")
        print("Result : {}".format(result))

    return result

def calc_minus(a: int, b: int):
    _IS_DEBUG = True
    if _IS_DEBUG: print("-------calc_minus-------start")
    result = a - b
    if _IS_DEBUG: 
        print("-------calc_minus-------end")
        print("Result : {}".format(result))

    return result

# 2. 중복 코드를 함수로 정리

def debug_log(isDebug: bool, m: str):
    if isDebug:
        print(m)

def calc_add1(a: int, b: int):
    debug_log(True, "-------calc_add1-------start")
    result = a + b
    debug_log(True, "-------calc_add1-------end")
    debug_log(True, "Result : {}".format(result))
    return result
    
def calc_minus1(a: int, b: int):
    debug_log(True, "-------calc_minus1-------start")
    result = a - b
    debug_log(True, "-------calc_minus1-------end")
    debug_log(True, "Result : {}".format(result))
    return result

# 3. 데코레이터 적용 1-1
def debug_log1(func):
    @functools.wraps(func)
    def wrappers(*args, **kwargs):
        _IS_DEBUG = True
        if _IS_DEBUG: print(f'------{func.__name__}-------start') # 문자열 출력시 f를 달아주면 해당 {} 안의 문자열은 변수명을 가리키게 된다. (string.format의 상위호환 기능)
        result = func(*args, **kwargs)
        if _IS_DEBUG: 
            print("Result : {}".format(result))
            print(f'------{func.__name__}-------end')
        return result

    return wrappers
    
@debug_log1
def calc_add2(a: int, b: int):
    return (a + b)

@debug_log1
def calc_minus2(a: int, b: int):
    return a - b

# 4. 데코레이터 적용 1-2 : decorator 선언시 인자값을 받을수 있도록 한번더 감싸준다.
def debug_log2(DEBUG_MODE=False):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            if DEBUG_MODE: print(f"------{func.__name__}------start")
            result = func(*args, **kwargs)
            if DEBUG_MODE: 
                print(f"Result : {result}")
                print(f"------{func.__name__}------end")
        return inner
    return decorator

@debug_log2(DEBUG_MODE=True)
def calc_add3(a: int, b: int):
    return (a + b)

# 기본적인 클로져의 모습
def annoy_o_tron(message):
    def greeting(name):
        print(f'{message} - {name}!!')

    return greeting

if __name__ == '__main__':
    calc_add2(5, 3)    
    calc_minus2(5, 3)    

    hello_o_tron = annoy_o_tron("Hello")    # 최초 변수 초기화시 annoy_o_tron함수가 실행 되면서 내부 함수를 리턴한 상태 이므로 해당 내부 함수는 print('Hello - {name}!!') 의 상태로 되어 있을 것이다. 
    #hello_o_tron() # 두가지의 변수중 하나만 값을 알고 있기 때문에 이대로 실행한다면 name 이라는 매개변수를 넘겨 달라는 오류가 발생한다.
    hello_o_tron("Jade.Lee")

    calc_add3(4, 6)

# 반복적으로 실행 되는 코드를 간결하게 만들고 싶은 경우 또는 첫번째 함수 실행의 결과에 따라 실행 되야 하는 고정 함수가 있는 경우 등등 응용할 곳이 많을거 같다.






