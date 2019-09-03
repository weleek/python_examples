#-*-coding:utf-8 -*-

import os, sys
import person_pb2 as messages

def prompt_for_person(person, code):
    """사용자의 입력을 받아 person 객체를 생성하여 반환 하는 함수
    """
    id, name  = '', ''
    while id is '': id = input('Enter the person ID: ')
    while name is '': name = input('Enter the person name: ')
    person.id, person.name, person.code = id, name, code
    #print(person.SerializeToString())                              # 직렬화
    #print(person.ParseFromString(person.SerializeToString()))      # 역직렬화
    return person 

if __name__ == '__main__':

    if len(sys.argv[:]) < 2:
        print(f'Usage : python {sys.argv[0]} [person count]')
        sys.exit(0)

    users = messages.Users()                # messages 모듈에 정의되어 있는 사용자 리스트를 객체를 선언
    for i in range(int(sys.argv[1])):       # 입력 횟수 만큼 루프
        prompt_for_person(users.users.add(), int(i) + 1)        # 해당 객체의 users 요소의 add 함수를 호출하여 인자로 전달

    print(users)

