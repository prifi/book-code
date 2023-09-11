# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/23 18:35
@Description: 
"""

"""
条件判断
    1.布尔值为假：''、None、0、False、[]、()、{}、set()、frozenset()
    2.布尔值为真：非 0 的数值、True，非空的序列、元组、字典，用户定义的类和实例
    3.三元表达式保持代码简洁，语法：true_value if <expression> else false_value（注意 or 陷阱： or None? 0?）
    4.仅在需要判断某个对象是否是 None、True、False 时，使用 is 运算符比较
    5.and 优先级 高于 or，使用括号让逻辑更清晰
    6.定义 __len__ (len(users)) 和 __bool__ (bool(ScoreJudger(59))) 魔法方法，可以自定义对象的布尔值规则。同时定义，优先使用bool 
    7.定义 __eq__ 方法，可以修改对象在进行 == 运算时的行为。is 判断内存地址，无法被重载
    
    ！整型驻留技术，-5 到 256 缓存内存数组，id(100) is id(200)，id(6300) is not id(6300)
    
条件分支
    1.“扁平优于嵌套” 要竭尽所能地避免分支嵌套，提前 return 返回
    2.别写太复杂的条件表达式，封装成函数或者对应的类方法
    3.尽量降低分支内代码的相似性，便于理解
    4.使用 all()/any() 函数构建条件表达式 all(n > 10 for n in numbers)
    5.“直译” 转 “意译”，bisect 模块可以用来优化范围类分支判断
        import bisect
        breakpoints = [10, 20, 30]
        bisect.bisect(breakpoints, 1)  # 0 -> 位于10之前，返回索引0
        bisect.bisect(breakpoints, 35) # 3 -> 位于30之后，返回索引3
    6.字典类型可以用来替代简单的条件分支语句
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
        'year': (lambda movie: movie.year, True),
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
        **extra_args,  # 使用字典扩展方式
    )