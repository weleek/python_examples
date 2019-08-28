#-*- coding: utf-8 -*-

# 예외 출력시 공통 함수 처리로 파일명과 라인번호를 좀 더 쉽게 찾기 위함.

import os, sys, linecache, traceback

def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    stk = traceback.extract_tb(tb, 1)
    f = tb.tb_frame
    lineno = tb.tb_lineno
    funcname = stk[0][2]
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print(f'\x1b[1;37;41m[EXCEPTION]\x1b[0m {exc_type.__name__}: Message "{exc_obj}", File "{filename}", Line {lineno}, in {funcname}\n\t{line.strip()}')

def start():
    try:
        print(1 / 0)
    except:
        print_exception()

if __name__ == '__main__':
    start()
    try:
        print(1/0)
    except:
        print_exception()

