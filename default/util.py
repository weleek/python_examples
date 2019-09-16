#-*- coding: utf-8 -*-

import time
from functools import wraps

# 함수 실행 시간 측정 함수. 데코레이터를 안쓰고 함수 형식으로 쓰는 경우 해당 방식 사용.
def timeit(f, *args, __=False, **kwargs):
    tick = time.perf_counter()
    res = f(*args, **kwargs)
    tock = time.perf_counter()
    msg = res is None and 'No returns' or res
    if __: msg = 'Off output'
    print(f'{f.__name__}:\n  {msg}  (took {1e3*(tock-tick):.6f} ms)')
    return res

def timer(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        msg = res is None and 'No returns' or res
        if msg != 'No returns': msg = 'Off output'
        print(f'{func.__name__}:\n  {msg}  (took {1e3*(end_time-start_time):.6f} ms)')
        return res
    return wrapper_func 


def test(count=1000):
    while count > 0:
        count = count - 1

@timer
def test2(count=1000):
    while count > 0:
        count = count - 1

@timer
def test3(count=1000):
    while count > 0:
        count = count - 1
    return count

if __name__ == '__main__':
    count = 100
    timeit(test, 10000, __=True)
    timeit(test, count, __=True)

    test2(count=10000)
    test2(count=count)

    test3(count=10000)
    test3(count=count)
