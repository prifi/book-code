# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/09/05 18:56
@Description: 
"""

"""
数据模型与描述符

    魔术方法：
        __getitem__          obj[key]            按索引读取
        __setitem__          obj[key] = value    按索引写入
        __delitem__          del obj[key]        按索引删除
        __len__              len(obj)            对象长度
        __bool__             bool(obj)           对象布尔值真假
        __eq__               obj == other.obj    == 运算时行为
        __enter__、__exit__  with obj:           上下文管理器行为
        __iter__、__next__   for _ in obj        对象被迭代行为
        __call__             obj()               被调用时行为
        __new__              obj_class()         创建实例时行为
    
    比较运算符 魔术方法
        __lt__      obj < other
        __le__
        __eq__
        __ne__
        __gt__
        __ge__
        
        使用 @total_ordering 让重载运算符变得更简单，自动补全剩下的所有方法
            只需 实现 __eq__ 和 __lt__、__le__、__gt__、__ge__ 四个方法之一即可 
    
    __del__ 魔术方法 慎用 它被作为垃圾回收时触发  ---用 with 语句来自动清理
        foo = Foo()
        l = [foo, ]
        del foo  # 此时不会触发 __del__ 方法，因为 foo 还有引用计数
"""


# 1.__str__、__repr__ 返回可读字符串

class Person:
    """人
    :param name: 姓名
    :param age: 年龄
    :param favorite_color: 最喜欢的颜色
    """

    def __init__(self, name, age, favorite_color):
        self.name = name
        self.age = age
        self.favorite_color = favorite_color

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{cls_name}(name={name!r}, age={age!r}, favorite_color={color!r})'.format(
            cls_name=self.__class__.__name__,
            name=self.name,
            age=self.age,
            color=self.favorite_color
        )


# 2.比较运算符魔术方法：计算正方形面积以及两个正方形实例是否相等

from functools import total_ordering

@total_ordering
class Square:
    """正方形

    :param length: 边长
    """

    def __init__(self, length):
        self.length =  length

    def area(self):
        return self.length ** 2

    def __eq__(self, other):
        # 在判断两个对象是否相等时，先检验 other 是否同为当前类型
        if isinstance(other, self.__class__):
            return self.length == other.length
        return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.length < other.length
        # 如果对象不支持某种运算，可以返回 NotImplemented 值
        return NotImplemented


# 3.两个文件（A, B）中有重合数据，找出在A里出现，但在B里没有的数据

# a.
def find_potential_customers_v2():
    """ 找到去过普吉岛但是没去过新西兰的人，性能改进版"""
    # 首先，遍历所有新西兰旅客记录，创建查找索引
    nz_records_idx = {
        (rec['first_name'], rec['last_name'], rec['phone_number'])
        for rec in users_visited_nz
    }
    for rec in users_visited_puket:
        key = (rec['first_name'], rec['last_name'], rec['phone_number'])
        if key not in nz_records_idx:
            yield rec

# b.
"""
>>> A = {1, 3, 5, 7}
>>> B = {3, 5, 8}
# 产生新集合：所有在 A 里但是不在 B 里的元素
>>> A - B
{1, 7}
"""

class VisitRecord:
    """旅客记录

    :param first_name: 名
    :param last_name: 姓
    :param phone_number: 电话号码
    :param date_visited: 旅游时间
    """
    def __init__(self, first_name, last_name, phone_number, date_visited):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.date_visited = date_visited

    # 解析实例不可哈希问题，TypeError: unhashable type: 'VisitRecord'
    def __hash__(self):
        return hash(self.comparable_fields)

    # 重写类型的 __eq__ 魔法方法（变为不可哈希，需要重写__hash__魔术方法），否则两个实例 == 为False
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.comparable_fields == self.comparable_fields
        return False

    @property
    def comparable_fields(self):
        """获取用于对比对象的字段值"""
        return (self.first_name, self.last_name, self.phone_number)

# 测试是否可哈希，是否相等
v1 = VisitRecord('a', 'b', phone_number='100-100-1000', date_visited='2000-01-01')
v2 = VisitRecord('a', 'b', phone_number='100-100-1000', date_visited='2000-01-01')
s = set()
s.add(v1)
s.add(v2)
print(s)         # {<__main__.VisitRecord object at 0x0000018EC9286430>, <__main__.VisitRecord object at 0x0000018EC9216CD0>}
print(v1 == v2)  # False Python只会判断是否指向内存中同一个地址

def find_potential_customers_v3():
    # 转换为 VisitRecord 对象后计算集合差值
    return set(VisitRecord(**r) for r in users_visited_puket) - set(VisitRecord(**r) for r in users_visited_nz)


# dataclasses 利用类型注解语法快速定义像上面的 VisitRecord 一样的数据类
from dataclasses import dataclass, field

@dataclass(frozen=True)
class VisitRecordDC:
    first_name: str
    last_name: str
    phone_number: str
    date_visited: str = field(compare=False)  # 不用于比较运算，跳过

def find_potential_custom_v4():
    return set(VisitRecordDC(**r) for r in users_visited_puket - set(VisitRecordDC(**r) for r in users_visited_nz))

