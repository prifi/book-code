# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/24 15:13
@Description: 
"""

"""
高阶函数（higher-order function）
闭包（closure）
装饰器（decorator）

函数的名字是否易读好记？dump_fields 是个好名字吗？
函数的参数设计是否合理？接收 4 个参数会太多吗？
函数应该返回 None 吗？

函数参数
    1.别将可变类型作为参数默认值：参数默认值只会在函数定义阶段被创建一次，正确的做法
        def append_value(value, items=None):
            if items is None:
                items = []
            items.append(value)
            return item
    2.“函数接收的参数不要太多，最好不要超过 3 个” --- 超过时，使用关键字参数提高代码可读性
        def foo(a, *, b, c)  # * 强制要求使用仅限关键字参数
            pass

函数返回
    1.尽量只返回一种类型 ---简单原则，返回单条或多条数据
    2.谨慎返回None值    ---除“搜索”“查询”场景，函数抛出异常（意料之外的结果）代替返回None更为合理
    3.早返回，多返回     ---一旦函数在执行过程中满足返回结果的要求，就直接返回

常用函数模块：functools
    1.functools.partial() 偏函数，将一些默认参数固定住，减少传递参数的效果：partial(func, *arg, **kwargs)
         partial_obj = partial(func, True, foo=1) ==> partial_obj() ==> func(True, foo=1)
    2.functools.lru_cache() 缓存功能，结果固定
        @lru_cache(maxsize=None)  # maxsize 最多可以保存多少个缓存结果，默认128，None表示每次执行结果都保存（内存溢出）
        def calculate_score(class_id):
            sleep(60)
            return 42

有状态函数：闭包或类方法
    1.闭包是一种允许函数访问已执行完成的其他函数里的私有变量的技术，是为函数增加状态的另一种方式
    2.类实例的状态一般都在 __init__ 函数里初始化
    
编程建议
    1.别写太复杂函数 ---65行
    2.函数分层设计 ---抽象层一致，拆分小函数
    3.优先使用列表推导式
        list(map(query_points, filter(lambda user: user.is_active(), users)))
        ===
        [query_points(user) for user in users ifuser.is_active()]  ---推荐
    4.递归限制较多，尽量使用循环来替代
"""

# 1.使用异常代替返回 None： 调用方可以从异常对象里获取错误原因
class UnableToCreateUser(Exception):
    """当无法创建用户时抛出"""

def create_user_from_name(username):
    """通过用户名创建一个 User 实例

    :raises: 当无法创建用户时抛出 UnableToCreateUser
    """
    if validate_username(username):
        return User.from_username(username)
    else:
        raise UnableToCreateUser(f'unable to create user from {username}')

def main():
    try:
        user = create_user_from_name(username='xiaotest')
    except UnableToCreateUser:
        # 此处编写异常处理逻辑
        pass
    else:
        user.do_something()


# 2.使用闭包的有状态替换函数: 将文件中数字以*，X交替替换展示
import re
def make_cyclic_mosaic():
    """将匹配到的模式替换为其他字符，使用闭包实现轮转字符效果"""
    char_index = 0
    mosaic_chars = ['*', 'X']

    def _mosaic(matchobj):
        nonlocal char_index
        char = mosaic_chars[char_index]
        char_index = (char_index + 1) % len(mosaic_chars)
        length = len(matchobj.group())
        return char * length

    return _mosaic


# 2.1 基于类实现有状态替换方法: 天生适合用来实现有状态对象
class CyclicMosaic:
    """使用会轮换的屏蔽字符，基于类实现"""
    _chars = ['*', 'x']

    def __init__(self):
        self._char_index = 0  # 类实例的状态一般都在 __init__ 函数里初始化

    def generate(self, matchobj):
        char = self._chars[self._char_index]
        self._char_index = (self._char_index + 1) % len(self._chars)
        length = len(matchobj.group())
        return char * length


re.sub(r'\d+', make_cyclic_mosaic(), '商店共 100 个苹果，小明以 12 元每斤的价格买走了')
re.sub(r'\d+', CyclicMosaic().generate, '商店共 100 个苹果，小明以 12 元每斤的价格买走了')
# 商店共 *** 个苹果，小明以 XX 元每斤的价格买走了
