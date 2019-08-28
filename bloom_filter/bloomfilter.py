#-*- coding: utf-8 -*-

# https://github.com/hiway/python-bloom-filter

from bloom_filter import BloomFilter

# 블룸필터 생성
have_met = BloomFilter(max_elements=10000, error_rate=0.1)

# 블룸필터에 존재한다면 True 반대라면 False 를 반환 하며 입력 받은 요소와 결과를 출력
def have_i_met(name):
    met = name in have_met
    print('Have I met {} before: {}'.format(name, met))

# 블룸필터에 요소 저장과 입력받은 요소를 출력
def meet(name):
    have_met.add(name)
    print('Hello, {}'.format(name))

# 테스트 요소인 이름을 3개를 입력 전과 입력 후로 테스트 한다.
for name in ['Harry', 'Larry', 'Moe']:
    have_i_met(name)
    meet(name)
    have_i_met(name)

print("Harr" in have_met)
print("Larr" in have_met)
print("Mo" in have_met)
