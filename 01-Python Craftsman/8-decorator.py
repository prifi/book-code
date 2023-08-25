# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/24 15:31
@Description: 
"""

"""
装饰器
    - 特殊高阶函数，修饰目标函数
    - 闭包原理实现
    - 使用 functools.wraps() 修饰包装函数
        @wraps(wrapped)
    - 实现可选参数装饰器
    - 用类来实现装饰器（函数替换）
    - 用类来实现装饰器（实例替换）

"""


# 1.有参装饰器
import time
from functools import wraps

def timer(print_args=False):
    """装饰器：打印函数耗时

    :param print_args: 是否打印方法名和参数，默认为 False
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            st = time.perf_counter()
            ret = func(*args, **kwargs)
            if print_args:
                print(f'"{func.__name__}", args: {args}, kwargs: {kwargs}')
                print('time cost: {} seconds'.format(time.perf_counter() - st))
            return ret
        return wrapper
    return decorator


# 2.可选参数的装饰器
def delayed_start(func=None, *, duration=1):
    """装饰器：在执行被装饰函数前，等待一段时间

    :param duration: 需要等待的秒数
    """
    def decorator(_func):
        def wrapper(*args, **kwargs):
            print(f'Wait for {duration} second before starting...')
            time.sleep(duration)
            return _func(*args, **kwargs)
        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)

# 调用方式
'''
# 1. 不提供任何参数
@delayed_start
def hello(): ...

# 2. 提供可选的关键字参数
@delayed_start(duration=2)
def hello(): ...

# 3. 提供括号调用，但不提供任何参数
@delayed_start()
def hello(): ...
'''


# 3.用类的方式重新实现了接收参数的 timer 装饰器
class timer:
    """装饰器：打印函数耗时

    :param print_args: 是否打印方法名和参数，默认为 False
    """

    def __init__(self, print_args):
        self.print_args = print_args

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            st = time.perf_counter()
            ret = func(*args, **kwargs)
            if self.print_args:
                print(f'"{func.__name__}", args: {args}, kwargs: {kwargs}')
            print('time cost: {:.2} seconds'.format(time.perf_counter() - st))
            return ret

        return decorated

@timer(True)
def xiaotest(name):
    time.sleep(3)
    print(f'hello, {name}.')

# xiaotest('xiaopf')

timer(True)(xiaotest)('xiaopf')
