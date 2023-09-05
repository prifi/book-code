# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/09/04 18:52
@Description: 
"""

"""
SOLID
    SRP：单一职责原则
    OCP：开放关闭原则  ---上两个针对 类和函数
    LSP: 里式替换原则  ---下三个仅针对 类
    ISP: 接口隔离原则
    DIP: 依赖倒置原则

LSP: 里式替换原则
    T(父) q(x) == S(子) q(y)
    LSP 能促使我们设计出更合理的继承关系，发挥多态
    
    - 子类随意抛出异常
        优化方法：通过继承显示的抛出自定义异常，抛出的异常属于父类协议的一部分
    - 子类随意调整方法参数与返回值
        1.返回值一致：LSP 要求子类方法的返回值类型与父类完全一致，或者返回父类结果类型的子类对象 issubclass(list, Iterable) -> True
        2.参数一致：子类的方法参数与父类相同，并且参数要求更为宽松（增加可选参数）、同名参数更抽象

DIP: 依赖倒置原则
    高层模块不应该依赖低层模块，二者都应该依赖抽象
    
    ! 只有对代码中那些容易变化的东西进行抽象，才能获得最大的收益。
    
ISP: 接口隔离原则
    - ISP 认为客户依赖的接口不应该包含任何它不需要的方法
    - 设计接口就是设计抽象
    - 写更小的类、更小的接口在大多数情况下是个好主意
    
    
"""

# 1.LSP: 子类随意抛出异常 优化 ---自定义异常
'''
# 自定义异常
class DeactivationNotSupported(Exception):
    """当用户不支持停用时抛出"""

# 父类
class User(Model):
    ...
    
    def deactivate(self):
        """停用当前用户
        
        :raises: 当用户不支持停用时，抛出 DeactivationNotSupported异常
        """
        pass

# 子类
class Admin(User):
    ...
    
    # 方法不支持禁用，抛出自定义异常
    def deactivate(self):
        raise DeactivationNotSupported('admin can not be deactivated')

# 调用时捕获自定义异常
def deactivate_users(users: Iterable[User]):
    """批量停用多个用户"""
    for user in users:
        try:
            user.deactivate()
        except DeactivationNotSupported:
            logger.info(f'user {user.username} does not allow deactivating, skip.' )
'''


# DIP:

# 统计 Hacker News 新闻来源分组脚本
import requests
from lxml import etree
from typing import Dict
from collections import Counter

class SiteSourceGrouper:
    """对 Hacker News 新闻来源站点进行分组统计

    :param url: Hacker News 首页地址
    """

    def __init__(self, url: str):
        self.url = url

    def get_groups(self) -> Dict[str, int]:
        """获取（域名，个数）分组"""
        resp = requests.get(self.url)
        html = etree.HTML(resp.text)
        elems = html.xpath('//table//tr[@class="athing"]//span[@class="sitestr"]')
        groups = Counter()
        for elem in elems:
            groups.update([elem.text])
        return groups

def main():
    groups = SiteSourceGrouper("https://news.ycombinator.com/").get_groups()
    for key, value in groups.most_common(3):
        print(f'Site: {key} | Count: {value}')

main()