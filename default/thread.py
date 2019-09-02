#-*- coding: utf-8 -*-

import os, sys
from threading import Thread
from threading import Lock

# 1. 기본 쓰레드 실험
class Counter:

    def __init__(self):
        self.count = 0  # 카운트 초기 값 0

    # 카운트를 1 올리는 함수
    def increment(self, offset):
        self.count += offset
        # 위의 함수식은 아래와 같이 풀이 된다.
        '''
        value = getattr(counter, 'count')   # counter = 카운터 클래스가 초기화 된 변수가 있다는 가정 이후에 진행: 해당 클래스로부터 count라는 이름을 가진 요소를 찾아서 value 변수에 값을 할당
        result = value + offset             # += 연산식을 이행하기 위해 result 변수에 value 값과 인자 값인 offset 을 더하여 초기화 한다.
        setattr(counter, 'count', result)   # 연산된 결과 값을 다시 counter 클래스의 count 요소에 값을 할당.
        '''


'''
실제 쓰레드로 동작 되는 함수.
sensor_index: 작업자 순번
how_many: 최대 작업 수치
counter: 작업 대상
'''
def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)

'''
실제 쓰레드를 할당하고 모두 작업이 완료되기를 대기하는 함수
func: 작업자 함수
how_many: 최대 작업 수치
counter: 작업 대상
'''
def run_threads(func, how_many, counter):
    threads = []                                        # 작업큐를 배열로 선언
    for i in range(5):                                  # 5개의 쓰레드를 동작하기 위한 for 문
        args = (i, how_many, counter)                   # 인자값 선언
        thread = Thread(target=func, args=args)         # 쓰레드 할당 
        threads.append(thread)                          # 작업큐에 넣어둔다.
        thread.start()                                  # 쓰레드를 시작한다. (무한루프 시작하며 각 순번에 해당 하는 함수들은 worker 함수가 시작)
    for thread in threads:                              # 쓰레드 작업큐에 담겨 있는 수만큼 for 문 동작
        thread.join()                                   # 해당 순번만큼 종료되길 기다리는 함수.

# 2. Lock 함수 적용 실험
class LockingCounter:

    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

# 테스트 메인 
if __name__ == '__main__':
                                                        # 1번 예제 시작.
    how_many = 10 ** 5                                  # 500000: 최대작업수치 50만
    counter = Counter()                                 # Counter: 클래스 선언 및 초기화
    run_threads(worker, how_many, counter)              # 메인 쓰레드 실행 함수 실행
    # 결과값 출력
    # 최대 출력치인 50만이 예상 출력치고 실제 counter 클래스가 가지고 있는 count변수의 값을 출력해본다.
    print('Counter should be %d, found %d' % (5 * how_many, counter.count))
    # 각 실행마다 같은 결과값이 나오지 않지만 
    # Counter should be 500000, found 442084
    # 원인은 최대 수치이 50만 까지만 실행을 하는 것이며 파이썬의 쓰레드는 병렬 처리로 보여지기 위해
    # 동작중인 쓰레드를 잠시 중지 하며 다음 쓰레드를 시작한다. 
    # 공평성을 유지 하기 위해 하나의 쓰레드를 모두 돌리지 않으며 연속적으로 중지와 시작을 반복하여 모든 쓰레드의 진행률을 맞춘다.
    '''
    # 스레드 A에서 실행함
    value_a = getattr(counter, 'count')
    # 스레드 B로 컨텍스트를 전환함
    value_b = getattr(counter, 'count')
    result_b = value_b + 1
    setattr(counter, 'count', result_b)
    #스레드 A로 컨텍스트를 되돌림
    result_a = value_a + 1
    setattr(counter, 'count', result_a)
    # 스레드 A는 스레드B에서 카운터 증가를 실행하는 모든 작업을 없애버립니다. 
    # a 에서 이전값이 할당된 상태로 b가 작업이 끝난후에 다시 a 가 실행하면 이전값이 증가된 상태가 아니기에 b의 작업은 결과적으로 무효화 된다.
    '''
    
    # 파이썬은 이와 같은 데이터 경쟁(race)과 다른 방식의 자료 구조 오염을 막으려고 내장 모듈 threading에 강력한 도구들을 갖춰놓고 있습니다. 
    # 가장 간단하고 유용한 도구는 상호 배제 잠금(뮤텍스) 기능을 제공하는 Lock 클래스입니다.
    # 잠금을 이용하면 여러 스레드가 동시에 접근하더라도 Counter 클래스의 현재 값을 보호할 수 있습니다. 한 번에 한 스레드만 잠금을 얻을 수 있습니다. 

    counter = LockingCounter()
    run_threads(worker, how_many, counter)
    print('Counter should be %d, found %d' % (5 * how_many, counter.count))
    # Counter should be 500000, found 500000



