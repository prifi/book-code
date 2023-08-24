# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/23 10:47
@Description: 
"""

"""
变量命名原则
    1.遵循PEP8原则
        - 应该用 4 个空格缩进，每行不超过 79 个字符
        - 蛇形命名法，比如 max_value，常量大写：MAX_VALUE
        - 内部变量加下划线：class_
        - 类名驼峰：FooClass
    2.描述性要强
        - “冬天的梅花” 描述 “花” 要强
        - file_chunks、pedding_id、active_number(s)
    3.要尽量短
        - 为变量命名要结合代码情境和上下文(level3_points)
    4.匹配类型
        - bool: is, has, allow, use 非黑即白，肯定或否定
            - is_superuser
            - has_errors
            - allow_empty
            - use_chrome
        - int/float 释义为数字
            - port, age, radius
            - _id 结尾: user_id, host_id
            - length/count 开头或结尾：max_length, length_of_username, users_count
            
            ! 不要用名词复数表示int类型，apples、trips容易与容器对象List(Apple)混淆，建议使用number_of_apples, trips_count复合词
    
        - 其他类型 ---建议使用变量注解
    5.超短命名
        - 数组索引三剑客 i、j、k
    

注释基础知识
    '''人
    :param name: 姓名
    :param age: 年龄
    :param favorite_color: 最喜欢的颜色
    :return: 人对象
    '''
    
    1.不要用注释屏蔽代码 ---Git仓库历史可找到
    2.不要用注释复述代码 
        - 描述代码为什么要这么做
        - 拆分函数，有意义的函数名达到了概括和指引作用
    3.不要弄错接口注释的受众 ---给使用者看，如何使用以及注意事项


编程建议
    1.保持变量一致性（名字一致性、类型一致性）
    2.变量尽量靠近使用
    3.定义临时变量提升可读性
    4.同一作用域内不要有太多变量，解决办法：提炼数据类、拆分函数
    5.能不定义变量就别定义
    6.显式优于隐式：不要使用 locals() 批量获取变量
    7.空行也是一种“注释”，增强代码可读性
    8.先写注释，后写代码
    
    ! 在写出一句有说服力的接口注释前，别写任何函数代码。
"""

# 1.代码可读性优化
from typing import List

def magic_bubble_sort(numbers: List[int]):
    """
    有魔力的冒泡排序算法，默认所有偶数比奇数大

    :param numbers: 需要排序的列表，函数会直接修改原始列表
    :return:
    """
    stop_position = len(numbers) - 1
    while stop_position > 0:
        for i in range(stop_position):
            current, next_ = numbers[i], numbers[i + 1]
            current_is_even, next_is_even = current % 2 == 0, next_ % 2 == 0
            shoud_swap = False

            # 交换位置两个条件：
            # - 前面是偶数，后面是奇数
            # - 前面和后面同为偶数或者奇数，但前面比后面大
            if current_is_even and not next_is_even:
                shoud_swap = True
            elif current_is_even == next_is_even and current > next_:
                shoud_swap = True

            if shoud_swap:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
        stop_position -= 1
    return numbers


# 2.同一作用域内不要有太多变量，对局部变量分组并建模
class ImportedSummary:
    """保存导入结果摘要数据类"""

    def __init__(self):
        self.succeeded_count = 0
        self.failed_count = 0


class ImportingUserGroup:
    """用户暂存用户导入的数据类"""

    def __init__(self):
        self.duplicated = []
        self.banned = []
        self.normal = []


def import_users_from_file(fp):
    """
    尝试从文件对象读取用户，然后导入数据库

    :param fp: 可读文件对象
    :return: 成功与失败的数量
    """
    import_user_group = ImportingUserGroup()
    for line in fp:
        parsed_user = parse_user(line)
        # ... 进行判断，修改 import_user_group 变量

    summary = ImportedSummary()
    #  ... 读取 import_user_group，写入数据库并修改成功与失败的数量

    return summary.succeeded_count, summary.failed_count
