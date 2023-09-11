# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/23 15:42
@Description: 
"""

"""
列表、元组、字典、集合
    1.可变（mutable）：列表、字典、集合。
    2.不可变（immutable）：整数、浮点数、字符串、字节串、元组
    
    ! Python 在进行函数调用传参时，采用的既不是值传递，也不是引用传递，而是传递了“变量所指对象的引用”  +=
    
    3.深拷贝与浅拷贝 import copy
        浅拷贝：
            - copy.copy(nums)
            - nums.copy()
            - 推导式
            - [:]
            - list(nums)、dict(d.items())
        深拷贝：[1, ['foo', 'bar'], 2, 3]
            - copy.deepcopy(items)
    
    4.使用字典、集合判断成员是否存在效率高 in notin O(1)
    5.不要编写过于复杂的推导式，用朴实的代码替代就好
    6.用按需返回替代容器，生成器 generator
    7.使用自定义字典优化代码
        - 当字典键不存在时，使用 defaultdict 可以简化处理; defaultdict(int) => key不存在不报错，调用int() => 0
        - 继承 MutableMapping 可以方便地创建自定义字典类，封装处理逻辑
    
列表
    1.有序、可变
    2.头部插入 collections.deque
    3.不要在遍历列表时同时修改

元组
    1.有序、不可变
    2.具名元组，比用普通数字（rect[0]）更易读、更好记
        from collections import namedtuple
        Rectangle = namedtuple('Rectangle', 'width,height')  # == namedtuple('Rectangle', ['width', 'height'])
        rect = Rectangle(width=100, height=20)  # rect[0]、rect.width
    3.让函数返回 NameTuple，便于后续扩展
        from typing import NamedTuple
        class Address(NamedTuple):
            country: str
        # addr.country
字典
    1.录入序、可变，key可哈希，唯一性
        from collections import OrderedDict # 无序的OrderedDict相比返回False, 无序dict返回True
    2.常用操作：
        dict.get(key, default) 
        dict.setdefault(key, default)  # d.setdefault('items', []).append('foo') 
        dict.pop(key, default)  # d.pop(key, None)
    3.快速合并字典 d3 = {**d1, **d2}
    4.不要在遍历字典时同时删除key
    
集合
    1.无序、可变，key可哈希，去重
    2.集合运算：
        & s1.intersection(s2)
        | s1.unicon(s2)
        - s1.difference(s2)
        
"""

# 1.分析网站访问日志
    # 格式：请求路径 请求耗时（毫秒）
    # /articles/three-tips-on-writing-file-related-codes/ 120
    # /articles/15-thinking-in-edge-cases/ 400
    # /admin/ 3275

# a.版本1
from enum import Enum

class PagePerfLevel(str, Enum):
    LT_100 = 'Less than 100 ms'
    LT_300 = 'Between 100 ms and 300 ms'
    LT_1000 = 'Between 300 ms and 1 s'
    GT_1000 = 'Greater than 1 s'

def analyze_v1():
    path_groups = {}
    with open('test_log.txt', 'r') as fp:
        for line in fp:
            path, time_cost_str = line.strip().split()

            # 根据页面耗时计算等级
            time_cost = int(time_cost_str)
            if time_cost < 100:
                level = PagePerfLevel.LT_100
            elif time_cost < 300:
                level = PagePerfLevel.LT_300
            elif time_cost < 1000:
                level = PagePerfLevel.LT_1000
            else:
                level = PagePerfLevel.GT_1000

            # 如果路径第一次出现，存入初始值
            # if path not in path_groups:
            # path_groups[path] = {}
            path_groups.setdefault(path, {})

            # 如果性能 level 第一次出现，存入初始值 1
            # try:
            #     path_groups[path][level] +=1
            # except KeyError:
            #     path_groups[path][level] = 1
            path_groups[path][level] = path_groups[path].get(level, 0) + 1

    for path, result in path_groups.items():
        print(f'== Path: {path}')
        total = sum(result.values())
        print(f'    Total requests: {total}')
        print(f'    Performance:')

        # 按照性能等级顺序排序输出，从小到大
        sorted_items = sorted(result.items(), key=lambda pair: list(PagePerfLevel).index(pair[0]))
        for level_name, count in sorted_items:
            print(f'        - {level_name}: {count}')

# b.版本2
    # - 当字典键不存在时，使用 defaultdict 可以简化处理; defaultdict(int) => key不存在不报错，调用int() => 0
    # - 继承 MutableMapping 可以方便地创建自定义字典类，封装处理逻辑

from collections import defaultdict
from collections.abc import MutableMapping

class PerfLevelDict(MutableMapping):
    """存储响应时间性能等级的字典"""

    def __init__(self):
        # defaultdict key不存在不报错，调用int() => 0
        self.data = defaultdict(int)

    # 操作前调用了 compute_level()，将字典键转成了性能等级
    def __getitem__(self, key):
        """当某个级别不存在时，默认返回 0"""
        return self.data[self.compute_level(key)]

    def __setitem__(self, key, value):
        """将 key 转换为对应的性能等级，然后设置值"""
        self.data[self.compute_level(key)] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    @staticmethod
    def compute_level(time_cost_str):
        """根据响应时间计算性能等级"""
        # 假如已经是性能等级，不做转换直接返回
        if time_cost_str in list(PagePerfLevel):
            return time_cost_str

        # 根据页面耗时计算等级
        time_cost = int(time_cost_str)
        if time_cost < 100:
            return PagePerfLevel.LT_100
        elif time_cost < 300:
            return PagePerfLevel.LT_300
        elif time_cost < 1000:
            return PagePerfLevel.LT_1000
        return PagePerfLevel.GT_1000

    def items(self):
        """按照顺序返回性能等级数据"""
        return sorted(self.data.items(), key=lambda pair: list(PagePerfLevel).index(pair[0]))

    def total_requests(self):
        """返回请求总数"""
        return sum(self.values())
        # return sum(self.data.values())


"""
# 测试：
>>> d = PerfLevelDict()
>>> d[50] += 1
>>> d[403] += 12
>>> d[30] += 2
>>> dict(d)
{<PagePerfLevel.LT_100: 'Less than 100 ms'>: 3,
<PagePerfLevel.LT_1000: 'Between 300 ms and 1 s'>: 12}
"""


def analyze_v2():
    path_groups = defaultdict(PerfLevelDict)  # 这句是关键，理解 defaultdict 模块用法
    with open('test_log.txt', 'r') as fp:
        for line in fp:
            path, time_cost_str = line.strip().split()

            # 如果key(path)不存在，生成新字典 path_greous[path] = PerfLevelDict()
            path_groups[path][time_cost_str] += 1

        for path, result in path_groups.items():
            print(f'== Path: {path}')
            print(f'    Total requests: {result.total_requests()}')
            print(f'    Performance:')
            for level_name, count in result.items():
                print(f'        - {level_name}: {count}')

analyze_v1()
analyze_v2()


# 2.使用生成器按需返回，更灵活，也更省内存
def generate_even(max_number):
    """一个简单生成器，返回 0 到 max_number 之间的所有偶数"""
    for i in range(0, max_number):
        if i % 2 == 0:
            yield i

for i in generate_even(10):
    print(i)


# 3.让函数返回 NamedTuple，增加返回值修改属性即可，便于扩展
from typing import NamedTuple

class Address(NamedTuple):
    """地址信息结果"""
    country: str
    province: str
    city: str

def latlon_to_address(lat, lon):
    return Address(
        country=country,
        province=province,
        city=city
    )

addr = latlon_to_address(lat, lon)
# 通过属性名来使用 addr
# addr.country / addr.province / addr.city
