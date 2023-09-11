# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/23 19:08
@Description: 
"""

"""
异常基础
    1.优先选异常捕获（EAFP：每次调用直接执行转换，返回结果）
    2.更精确到 except 语句放在前面，异常的继承关系，父覆盖子
    3.try/except .. finally 无论如何都会执行finally，即时执行了return
    4.try/except .. else
        - 没有发生异常执行else，替换标记变量flag
        - 与finally不同，如果提前return或break，else语句不会执行
    5.自定义异常类：抛出(raise)异常，而不是返回错误
        class CreateItemError(Exception):
            '''创建 Item 失败'''
        raise CreateItemError('items is full')
    6.使用上下文管理器(with)简化异常处理  ---示例2、3、4
        - 用于替代 finally 语句清理资源
        - 对异常二次处理后重新抛出 或 忽略异常
        - 使用 contextmanager 装饰器 yield

编程建议
    1.不要随意忽略异常，针对异常的最佳实践
        - 在 except 语句捕获并处理
        - 在 except 语句捕获，将错误通知终端用户，中断执行
        - 在 except 语句捕获，通过日志记录下这个异常
        - 不捕获异常，让异常往堆栈上层走
        
        ！“除非有意静默，否则不要无故忽视异常。”
        
    2.不要手动做数据校验，专业的数据校验模块：pydantic 库校验  ---示例5
        from pydantic import BaseModel
        class NumberInput(BaseModel):
            # 使用类型注解 conint 定义 number 属性的取值范围
            number: conint(ge=0, le=100)
    3.抛出可区分的异常：自定义异常子类或者异常代码(error_code) ---示例1.1
    4.使用“空对象模式”捕获异常并处理：创建空对象实例 NullUserPoint()
        class NullUserPoint:
            # 一个空的用户得分记录
            username = ''
            points = 0
            
            def is_qualified(self):
                return False

常见异常
    KeyboardInterrupt       Ctrl+C中断脚本异常
    TypeError               类型异常
    ValueError              值异常
    AttributeError          属性异常
    RequestException        requests请求异常
    IOError                 文件写入异常
"""

# 1.自定义异常类：抛出异常，而不是返回错误
class CreateItemError(Exception):
    """创建 Item 失败"""

# 1.1 异常子类
class CreateErrorItemsFull(CreateItemError):
    """当前 Item 容器已满"""

# 1.1 异常代码：根据异常对象的 error_code 来精确分辨异常类型
'''
class CreateItemError(Exception):
    """创建 Item 失败
    :param error_code: 错误代码
    :param message: 错误信息
    """
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message
        super().__init__(f'{self.error_code} - {self.message}')

# 抛出异常时指定 error_code
raise CreateItemError('name_too_long', 'name of item is too long')
raise CreateItemError('items_full', 'items is full')
'''

def create_item(name):
    """创建一个新的 Item

    :param name:
    :raises: 当无法创建时抛出 CreateItemError
    """
    if len(name) > MAX_LENGTH_OF_NAME:
        raise CreateItemError('name of item is too long')
    if len(get_current_items()) > MAX_ITEMS_QUOTA:
        # raise CreateItemError('items is full')      # 抛出父类异常
        raise CreateErrorItemsFull('items is full')   # 抛出子类异常，更精确
    return Item(name=name), ''

def create_from_input():
    name = input()
    try:
        item = create_item(name)
    except CreateErrorItemsFull as e:
        clear_all_items()
        print(f'create item failed: {e}')
    except CreateItemError as e:
        print(f'create item failed: {e}')
    else:
        print(f'item<{name}> created')


# 2.使用上下管理器: 替代 finally 语句清理资源
class create_conn_obj:
    """创建连接对象，并在退出上下文时自动关闭"""

    def __init__(self, host, port, timeout=None):
        self.conn = create_conn(host, port, timeout=timeout)

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # __exit__ 会在管理器退出时调用
        self.conn.close()
        return False

# 使用上下文管理器创建连接
with create_conn_obj(host, port, timeout=None) as conn:
    try:
        conn.send_text('Hello, world!')
    except Exception as e:
        print(f'Unable to use connection: {e}')


# 3.使用上下管理器: 忽略已经关闭的连接异常
class ignore_closed:
    """忽略已经关闭的连接"""
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == AlreadyClosedError:
            return True  # 异常压制
        return False  # 正常抛出

with ignore_closed():
    close_conn(conn)


# 4.使用上下管理器: 使用 contextmanager 装饰器
from contextlib import contextmanager

@contextmanager
def create_conn_obj(host, port, timeout=None):
    """创建连接对象，并在退出上下文时自动关闭"""
    conn = create_conn(host, port, timeout=timeout)  # 类似于 __enter__
    try:
        yield conn
    finally:
        conn.close()  # 类似于 __exit__


# 5.使用 pydantic 库校验输入数据
from pydantic import BaseModel, conint, ValidationError

class NumberInput(BaseModel):
    # 使用类型注解 conint 定义 number 属性的取值范围
    number: conint(ge=0, le=100)

def input_a_number_with_pydantic():
    while True:
        number = input('Please input a number (0-100): ')
        # 实例化为 pydantic 模型，捕获校验错误异常
        try:
            number_input = NumberInput(number=number)
        except ValidationError as e:
            print(e)
            continue
        number = number_input.number
        break
    print(f'Your number is {number}')