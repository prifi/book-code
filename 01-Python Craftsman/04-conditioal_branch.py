# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/23 18:35
@Description: 
"""

"""
条件判断
    - 布尔值为假：'', None、0、False、[]、()、{}、set()、frozenset()
    - 布尔值为真：非 0 的数值、True，非空的序列、元组、字典，用户定义的类和实例
    - 三元表达式保持代码简洁 1 or 2
    - 仅在需要判断某个对象是否是 None、True、False 时，使用 is 运算符
    - and 优先级 高于 or，使用括号让逻辑更清晰
    
条件分支：
    - “扁平优于嵌套” 要竭尽所能地避免分支嵌套，提前 return 返回
    - 别写太复杂的条件表达式，封装成函数或者对应的类方法
    - 尽量降低分支内代码的相似性
    - 使用 all()/any() 函数构建条件表达式
"""

# 1.消失的分支 ---“直译” 转 “意译”
    # - bisect 模块可以用来优化范围类分支判断
    # - 字典类型可以用来替代简单的条件分支语句

import bisect
import random

class Movie:
    """电影对象数据类"""

    def __init__(self, name, year, rating):
        self.name = name
        self.year = year
        self.rating = rating

    @property
    def rank(self):
        """
        按照评分对电影分级

        :return:
        """
        # 已经排好序的评级分界点
        breakpoints = (6, 7, 8, 8.5)
        # 各评分区间级别排名
        grades = ('D', 'C', 'B', 'A', 'S')

        index = bisect.bisect(breakpoints, float(self.rating))
        return grades[index]

def get_sorted_movies(movies, sorting_type):
    """
    对电影列表进行排序并返回

    :param movies: Movie 对象列表
    :param sorting_type: 排序选项，可选值：name(名称)、rating(评分)、year(年份)、random(随机乱序)
    :return:
    """
    sorting_algos = {
        # sorting_type: (key_func, reverse)
        'name': (lambda movie: movie.name.lower(), False),
        'rating': (lambda movie: movie.rating, True),
        'year': (lambda movie: movie.name, True),
        'random': (lambda movie: random.random(), False)
    }
    try:
        key_func, reverse = sorting_algos[sorting_type]
    except KeyError:
        raise RuntimeError(f'Unknow sorting type: {sorting_type}')

    sorted_movies = sorted(movies, key=key_func, reverse=reverse)
    return sorted_movies


# 2.尽量降低分支内代码的相似性

def create_or_update():
    if user.no_profile_exists:
        _update_or_create = create_user_profile
        extra_args = {'points': 0, 'created': now()}
    else:
        _update_or_create = update_user_profile
        extra_args = {'updated': now()}

    _update_or_create(
        username=user.username,
        gender=user.gender,
        email=user.email,
        age=user.age,
        address=user.address,
        **extra_args,
    )