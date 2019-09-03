#-*- coding:utf-8 -*-

import os, sys, timeit, random
from functools import wraps
from threading import Thread

# 함수 동작 실행 시간 출력 데코레이터
def timer(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        #print(f"{func.__name__} Elapsed time: {end_time - start_time}")
        print('{} Elapsed time: {}'.format(func.__name__, (end_time - start_time)))
        return result
    return wrapper_func

def work(n):
    while n>0:
        n -= 1

# 1. single thread
@timer
def single_thread(n):
    work(n)

# 2. multi thread
@timer
def multi_thread(n):
    threads = []
    thread_num = 2
    for i in range(thread_num):
        t = Thread(target=work, args=(COUNT//thread_num,))
        threads.append(t)
        t.start()

    for i in threads:
        i.join()

if __name__ == '__main__':
    COUNT = 50000000
    
    single_thread(COUNT)

    multi_thread(COUNT)
