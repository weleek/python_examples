# -*- coding:utf-8 -*-

import pytest


# default
class Person:
    # 해당 객체의 값을 추가 할 경우 추가될 수 있도록 __dict__ 공간을 만들어 두는데
    # 해당 속성에 인스턴스 변수를 명시 해 놓는 다면 다른 이름의 인스턴스 변수가 생성 되는 걸 제한 함으로
    # __dict__ 속성을 만들 필요가 없어짐으로 성능 향상을 꾀 할 수 있다.
    __slots__ = ("name", "lastname")  # __slots__ : 인스턴스 변수 생성 추가시 생성 가능한 속성을 제한 할 수 있다.

    d_lastname = "Lee"  # slots에 정의 되어 있지 않는 변수명에 대해 static 변수로 설정 가능.

    def __init__(self, name="Jade"):
        self.name = name  # 클래스 인스턴스 변수 : 인스턴스화 이후에 사용 가능.
        self.lastname = self.d_lastname
        # self.ddd = 'test'                  # slots에 정의 되어 있지 않는 인스턴스 속성 추가 불가.

    def hello(self, word="Hello"):
        print(f"{word}, {self.name}.{self.lastname}!")


def test_person():
    print(Person.d_lastname)  # 스태틱 변수로 선언 되었기 때문에 인스턴스화 시키지 않고서도 접근이 가능하다.
    p = Person()
    p.hello()
    print(p.name)  # 인스턴스 변수 접근 가능.
    print(p.lastname)

    print(Person)
    print(dir(p))
    assert 0