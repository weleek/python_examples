# -*- coding: utf-8 -*-

obj = {
    1: True,                # AND right     , OR left
    2: False,               # AND left      , OR right
    3: None,                # AND left      , OR right
    4: 'string',            # AND right     , OR left
    5: '',                  # AND left      , OR right
    6: 123456789            # AND right     , OR left
}



def and_function(idx: int):
    return obj[idx] and 'TEST'


def or_function(idx: int):
    return obj[idx] or 'TEST'


if __name__ == '__main__':
    # 변수 선언시 javascript 처럼 || 조건으로 초기화가 가능하다.
    A = None
    B = A or 1

    #print(A)   # output : None
    #print(B)   # output : 1

    # 반환 객체에 조건식을 사용했을 경우 아래와 같은 결과를 얻을수 있다.
    print(f'RETURN AND {"== ==" * 20}')
    for i in range(1, 7):
        print(and_function(int(i)))

    print(f'RETURN OR {"== ==" * 20}')
    for i in range(1, 7):
        print(or_function(int(i)))

    # 반환값 또는 객체에 조건을 사용시 and 를 준 경우 왼쪽부터 순서대로 False, None, '' 에 해당하지 않으면 마지막 값
    # 또는 객체를 반환하며 or 를 준 경우 마지막 순서까지 가지 않아도 반환 된다.

    # 폴더 목록 리스트중 날짜 형식으로 된 폴더명만을 가져와서 정렬한다.
    ls = '''drwxrwxr-x 2 ubuntu ubuntu 4096 2018-10-16 00:00:00 2018-10-1
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-10-18 00:00:06 2018-10-17
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-11-01 00:00:04 2018-10-18
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-12-06 00:00:03 2018-11-1
    drwxrwxr-x 2 ubuntu ubuntu 4096 2019-01-06 00:00:04 2018-12-29
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-12-29 01:19:52 2018-12-6
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-07-02 00:00:00 2018-6-29
    drwxrwxr-x 2 ubuntu ubuntu 4096 2019-04-24 03:06:44 2018-6-4
    drwxr-xr-x 2 ubuntu root   4096 2018-08-08 00:00:01 2018-7-17
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-07-04 00:00:00 2018-7-2
    drwxr-xr-x 2 ubuntu root   4096 2018-07-05 00:00:01 2018-7-4
    drwxr-xr-x 2 ubuntu root   4096 2018-07-06 00:00:00 2018-7-5
    drwxr-xr-x 2 ubuntu root   4096 2018-07-17 00:00:03 2018-7-6
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-08-25 00:00:00 2018-8-18
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-08-27 00:00:00 2018-8-25
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-09-01 00:00:00 2018-8-27
    drwxr-xr-x 2 ubuntu root   4096 2018-08-18 00:00:05 2018-8-8
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-09-07 00:00:00 2018-9-1
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-10-01 00:00:03 2018-9-10
    drwxrwxr-x 2 ubuntu ubuntu 4096 2018-09-10 00:00:01 2018-9-7
    drwxrwxr-x 2 ubuntu ubuntu 4096 2019-04-04 00:00:14 2019-1-6
    drwxrwxr-x 2 ubuntu ubuntu 4096 2019-10-12 00:00:03 2019-10-1
    drwxrwxr-x 2 ubuntu ubuntu 4096 2019-10-15 00:00:01 2019-10-12
    drwxrwxr-x 2 ubuntu ubuntu 4096 2019-10-21 00:00:01 2019-10-15
    drwxrwxr-x 2 ubuntu ubuntu 4096 2019-06-17 00:00:08 2019-4-4
    drwxrwxr-x 2 ubuntu ubuntu 4096 2019-10-01 00:00:07 2019-6-17'''
    print(ls)

    result_dict = dict(map(lambda x: (" ".join(x.split(" ")[-3:-1]), x.split(" ")[-1]), ls.split('\n')))

    for k, v in result_dict.items():
        print(f'{k} : {v}')

    print(result_dict[sorted(result_dict, reverse=True)[0]])

    result_list = list(map(lambda x: x.split(" ")[-1], ls.split("\n")))

    print(result_list)
    from datetime import datetime
    result_list.sort(reverse=True, key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
    print(result_list)
