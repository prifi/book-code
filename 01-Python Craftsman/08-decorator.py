# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/24 15:31
@Description: 
"""

"""
装饰器
    - 特殊高阶函数，修饰目标函数
    - 闭包原理实现（返回函数）
    - 使用 functools.wraps() 修饰包装函数
        @wraps(func)
    - 实现可选参数装饰器
    - 用类来实现装饰器（函数替换）
    - 用类来实现装饰器（实例替换）
    - 使用 wrapt 模块助力装饰器编写 ---类装饰器注入第一参数 self
    
装饰器本质：
    - 运行时校验：django: @login_required
    - 注入额外参数
    - 缓存执行结果：@lru_cache
    - 注册函数：flask: @app.route
    - 替换为复杂对象: @staticmethod
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


# 3.用类的方式重新实现了接收参数的 timer 装饰器（类方法实现）
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

# xiaotest('xiaopf') # ==> timer(True)(xiaotest)('xiaopf')


# 4.实例替换的无参数装饰器 DelayedStart（类实例实现）
from functools import update_wrapper
class DelayedStart:
    """在执行被装饰函数前，等待1秒钟"""

    def __init__(self, func):
        update_wrapper(self, func)  # 把被包装函数元数据更新到包装者
        self.func = func

    def __call__(self, *args, **kwargs):
        print('Wait for 1 second before starting...')
        time.sleep(1)
        return self.func(*args, **kwargs)

    def eager_call(self, *args, **kwargs):  # 为装饰器提供额外方法，提供多样化接口
        """跳过等待，立即执行被装饰函数"""
        print('Call without delay')
        return self.func(*args, **kwargs)

@DelayedStart
def hello():
    print('Hello World.')

# 被装饰的 hello 函数已经变成了装饰器类 DelayedStart 的实例
# print(hello)  # <__main__.DelayedStart object at 0x7f048cc78b70>
# print(type(hello))  # <class '__main__.DelayedStart'>
#
# hello()
# hello.eager_call()


# 5.实例替换的有参数装饰器（类实例实现）
# 为 DelayedStart 增加了控制调用延时的 duration 参数
class DelayedStart:
    """在执行被装饰函数前，等待一段时间
    :param func: 被装饰函数
    """

    def __init__(self, func, *, duration=1):
        update_wrapper(self, func)
        self.func = func
        self.duration = duration

    def __call__(self, *args, **kwargs):
        print(f'Wait for {self.duration} second before starting...')
        time.sleep(self.duration)
        return self.func(*args, **kwargs)

    def eager_call(self, *args, **kwargs):
        """跳过等待，立即执行被装饰函数"""
        print('Call without delay')
        return self.func(*args, **kwargs)

import functools
def delayed_start(**kwargs):
    """装饰器：推迟某个函数执行"""
    return functools.partial(DelayedStart, **kwargs)

@delayed_start(duration=2)
def hello():
    print('Hello World.')

# hello()
# hello.eager_call()


# 6.自动注入函数参数的装饰器 ---被调用时自动生成一个随机数，并将其注入为函数的第一个位置参数
    # 问题：普通函数调用时正常，类方法调用时会将self注入第一参数
    # 解决：基于 wrapt 模块解决类方法第一参数注入问题 (self, num)
import wrapt
import random

def provide_number(min_num, max_num):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, **kwargs):
        # 参数含义：
        #
        # - wrapped：被装饰的函数或类方法
        # - instance：
        # - 如果被装饰者为普通类方法，则该值为类实例
        # - 如果被装饰者为 classmethod 类方法，则该值为类
        # - 如果被装饰者为类/函数/静态方法，则该值为 None
        #
        # - args：调用时的位置参数（注意没有 * 符号）
        # - kwargs：调用时的关键字参数（注意没有 ** 符号）
        #
        num = random.randint(min_num, max_num)
        # 无须关注 wapped 是类方法还是普通函数，直接在头部追加参数
        args = (num,) + args
        return wrapped(*args, **kwargs)
    return wrapper

"""
>>> print_random_number()
22
>>> Foo().print_random_number()
93
"""
