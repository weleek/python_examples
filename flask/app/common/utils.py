# -*- coding: utf-8 -*-
import os
import sys
import linecache
import traceback


def print_stack_trace():
    exc_type, exc_obj, tb = sys.exc_info()
    stk = traceback.extract_tb(tb, 1)
    f = tb.tb_frame
    lineno = tb.tb_lineno
    funcname = stk[0][2]
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print(f'\x1b[1;37;41m[EXCEPTION]\x1b[0m {exc_type.__name__}: ', end='')
    print(f'Message "{exc_obj}", File "{filename}", Line {lineno}, in {funcname}\n\t{line.strip()}')
