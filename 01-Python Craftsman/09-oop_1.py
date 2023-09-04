# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/31 16:57
@Description: 
"""

"""
面向对象编程
    
封装、继承、多态

封装：
    - 私有属性： __{var} ---访问：_{class}__{var}
    - 实例字典与类字典：p.__dict__, Person.__dict__
        setattr(p, key, value)

内置类方法装饰器
    - 类方法 @classmethod ---定义工厂方法来生成新实例 return cls(color=color)
    - 静态方法 @staticmethod ---不需要使用实例里的任何内容
    
    ! 类和实例都可调用 类方法 和 静态方法
    
    - @property 将方法转换为类属性方式调用

继承：
    - 多用组合，少用继承
    - 多重继承与 MRO: D.mro() ---广度优先
    - 针对事物的行为建模，而不是对事物本身建模
        1.读取日志
        2.解析日志
        3.统计日志 yield
            def __init__(self, date):
                self.date = date
                self.log_reader = LogReader(self.date)
                self.log_parser = LogParser()
    - 继承是一种紧耦合关系，继承时应考虑：
        1.子继承父，是否是同类型(int? list?)？
        2.是否需要继承来表明类型关系？ ---鸭子类型
        3.子类只是复用父类方法，组合替代继承是否会更好？

预绑定方法模式（prebound method pattern）是一种将对象方法绑定为函数的模式

"""

# 1.类方法使用 ---定义工厂方法来生成新实例
import random

class Duck:

    def __init__(self, color):
        self.color = color

    @classmethod
    def create_random(cls):
        """创建一只随机颜色的鸭子"""
        color = random.choice(['yellow', 'white', 'gray'])
        return cls(color=color)

    def quack(self):
        print(f"Hi, I'm a {self.color} duck!")

d = Duck.create_random()
d.quack()
# print(d.create_random())  # 实例方式调用


# 2.使用 @property 装饰器，把方法通过属性的方式暴露
    # - 定义 setter 方法，该方法会在对属性赋值时被调用
    # - 定义 deleter 方法，该方法会在删除属性时被调用
import os

class FilePath:

    def __init__(self, path):
        self.path = path

    @property
    def basename(self):
        """获取文件名"""
        return self.path.rsplit(os.sep, 1)[-1]

    @basename.setter
    def basename(self, name):
        """修改当前路径里的文件名部分"""
        new_path = self.path.rsplit(os.sep, 1)[:-1] + [name]
        self.path = os.sep.join(new_path)

    @basename.deleter
    def basename(self):
        raise RuntimeError('Can not delete basename!')

p = FilePath('/tmp/foo.py')
print(p.basename)  # foo.py
p.basename = 'bar.txt'
print(p.path)  # /tmp/bar.txt


# 3.实现单例模式，只需在模块里创建一个全局对象
class AppConfig:
    """程序配置类，使用单例模式"""

    def __init__(self):
        # 省略：从外部配置文件读取配置
        pass

    def get_database(self):
        # 获取数据库配置
        pass

    def reload(self):
        # 刷新配置
        pass

_config = AppConfig()
get_database_conf = _config.get_database
reload_config = _config.reload
# from config import get_database_conf
# data_conf = get_database_conf()
# reload_config()