# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/24 11:11
@Description: 
"""

"""
迭代器与可迭代对象
    1.iter() 与 next()，for 循环的工作原理
        iterator = iter(names)
        while True:
            try:
                name = next(iterator)
                print(name)
            except StopIteration:
                break
    2.自定义迭代器
        - 可迭代对象不一定是迭代器，但迭代器一定是可迭代对象
        - 对可迭代对象使用 iter() 会返回迭代器，迭代器则会返回其自身
        - 每个迭代器的被迭代过程是一次性的，可迭代对象则不一定
        - 可迭代对象只需要实现 __iter__ 方法，而迭代器要额外实现 __next__ 方法 ---示例1
    3.生成器是迭代器：一种简化的迭代器实现 yield
        - 通过修饰可迭代对象来优化循环: enumerate() 函数的思路  ---示例2
    4.使用 itertools 模块优化循环
        - 遍历多个对象的多层循环代码，使用 product() 函数优化
            from itertools import product
            list(product([1, 2], [3, 4]))
            # [(1, 3), (1, 4), (2, 3), (2, 4)]  # 笛卡儿积不断生成结果
        - 使用 islice() 实现循环内隔行处理：islice(seq, start, end, step)
            # 设置 step=2，跳过无意义的 --- 分隔符
            for line in islice(fp, 0, None, 2):
                 yield line.strip()
        - 使用 takewhile() 替代 break 语句：提前结束循环
            from itertools import takewhile
            takewhile(predicate, iterable)  # 调用 predicate() 对 iterable 元素做真值测试，False中断本次迭代
            
            # 示例
            for user in takewhile(is_qualified, users):  # 多参数可以使用偏函数
                # 进行处理……
        - 用 chain() 函数可以扁平化双层嵌套循环、用 zip_longest() 函数可以同时遍历多个对象，等等。
    5.(for/while)循环语句的 else 关键字 ---正常循环完没有碰到任何break，执行else（提前return不执行else）  ---示例4
        ! “拆分子函数”的技巧来重构
    6.使用 while 循环加 read() 方法分块读取大文件内容
    7.iter() 的另一个用法 ---示例5
        - iter(callable, sentinel) 用循环遍历这个迭代器，会不断返回调用 callable() 的结果，假如结果等于sentinel，迭代过程中止
            # 使用 functools.partial 构造一个新的无须参数的函数
            _read = partial(fp.read, block_size)
            iter(_read, '')
        - 拆分 “数据生成” 和 “数据消费” 逻辑 yield

编程建议
    1.循环过于复杂？ ---按职责分类，抽象成独立的生成器（或迭代器）
    2.中断嵌套循环的正确方式：不要使用多个break，拆分为函数使用 return 更好
    3.巧用next()函数: next(iter(d.keys())) 取出字典的第一个key
    4.当心已被耗尽的迭代器：生成器（迭代器）“可被一次性耗尽”
"""

# 1.自定义迭代器: Range7 类型可以被重复迭代
class Range7:
    """生成某个范围内可被 7 整除或包含 7 的数字"""
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        # 返回一个新的迭代器对象
        return Range7Iterator(self)

class Range7Iterator:
    def __init__(self, range_obj):
        self.range_obj = range_obj
        self.current = range_obj.start

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self.current >= self.range_obj.end:
                raise StopIteration

            if self.num_is_valid(self.current):
                ret = self.current
                self.current += 1
                return ret
            self.current += 1

    def num_is_valid(self, num):
        if num == 0:
            return False
        return num % 7 == 0 or '7' in str(num)


# 2.使用生成器函数修饰可迭代对象: enumerate() 函数的思路
def sum_even_only(numbers):
    """对 numbers 里面所有偶数求和"""
    result = 0
    for num in numbers:
        if num % 2 == 0:
            result += num
    return result

# a.创建生成器函数 even_only()，它专门负责偶数过滤工作：
def even_only(numbers):
    for num in numbers:
        if num % 2 == 0:
            yield num

# b.用 even_only() 函数修饰 numbers 变量 “偶数过滤”，实现求和：
def sum_even_only_v2(numbers):
    """对 numbers 里面所有偶数求和"""
    result = 0
    for num in even_only(numbers):
        result += num
    return result


# 3.扁平优于嵌套
def find_twelve(num_list1, num_list2, num_list3):
    """从 3 个数字列表中，寻找是否存在和为 12 的 3 个数"""
    for num1 in num_list1:
        for num2 in num_list2:
            for num3 in num_list3:
                if num1 + num2 + num3 == 12:
                    return num1, num2, num3

# 用 product() 优化函数里的嵌套循环：
from itertools import product
def find_twelve_v2(num_list1, num_list2, num_list3):
    for num1, num2, num3 in product(num_list1, num_list2, num_list3):
        if num1 + num2 + num3 == 12:
            return num1, num2, num3

# 4.循环中的else子句
def foo():
    for i in range(7):
        print(i)
        if i == 4:
            return i  # 提前返回不执行else
        if i == 5:
            break
    else:
        print('done')


# 5.数字统计任务：计算某个文件中数字字符（0～9）的数量（5GB大文件）
    # 标准做法：with open (fine_name) 上下文管理器语法获得文件对象，使用循环遍历
        # - 自动关闭文件描述符
        # - 逐行获取内容，\n
    # 弊端：内容中无换行符，一次性返回大文件内容，消耗时间和内存

# a.使用 while 循环加 read() 方法分块读取
def count_digits(fname):
    """计算文件里包含多少数字字符，每次读取8KB"""
    count = 0
    block_size = 1024 * 8
    with open(fname) as file:
        while True:
            chunk = file.read(block_size)
            # 当文件没有更多内容时，read 调用将返回空字符串 ''
            if not chunk:
                break
            for s in chunk:
                if s.isdigit():
                    count += 1
    return count

# b.用 iter() 读取文件
from functools import partial

def count_digits_v2(fname):
    count = 0
    block_size = 1024 * 8
    with open(fname) as fp:
        # 使用偏函数，构造无参数函数
        _read = partial(fp.read, block_size)

        # 利用 iter() 构造不断调用 _read 的迭代器
        for chunk in iter(_read, ''):
            for s in chunk:
                if s.isdigit():
                    count += 1
    return count


# 5.1 数字统计任务：统计文件里面所有偶数字符 (0, 2, 4, 6, 8) 出现的次数
    # - 解耦循环体，使用生成器

# 生成器：复用已有的“按块读取大文件”的功能
def read_file_digits(fp, block_size=1024 * 8):
    """生成器函数：分块读取文件内容，返回其中数字字符"""
    _read = partial(fp.read, block_size)
    for chunk in iter(_read, ''):
        for s in chunk:
            if s.isdigit():
                yield s      # 这句是关键
# 统计数字
def count_digits_v3(fname):
    count = 0
    with open(fname) as file:
        for _ in read_file_digits(file):
            count += 1
    return count

# 统计偶数
from collections import defaultdict

def count_even_groups(fname):
    counter = defaultdict(int)
    with open(fname) as file:
        for num in read_file_digits(file):
            if int(num) % 2 == 0:
                counter[num] += 1
    return counter
