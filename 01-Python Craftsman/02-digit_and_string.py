# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/08/23 14:59
@Description: 
"""

"""
数值
    1.浮点数精度问题
        0.1 + 0.2 => 0.30000000000000004
        解决办法：
            from decimal import Decimal
            Decimal('0.1') + Decimal('0.2') # 注意是字符串
    2.布尔值也是数字(0 和 1) ---短路运算
        # 计算列表里一共有多少个偶数
        count = sum(i % 2 == 0 for i in numbers)

字符串
    1.不常用但特别好用的字符串方法
        - str.partition(sep)
        - str.translate(s.maketrans(',.', '，。'))  # 一次性替换多个字符
    2.字符串和字节串
        str.encode(codec) 计算机层 bytes二进制字符串
        str.decode(codec) 人类层 str普通字符串
    3.改善长字符串可读性，使用(), \, 多行缩进使用模块 textwrap.dedent() 
"""

# 1.使用枚举增强代码可读性与健壮性

from enum import Enum

# 在定义枚举类型时，如果同时继承一些基础类型，比如 int、str,
# 枚举类型就能同时充当该基础类型使用。比如在这里, UserType 就可以当作 int 使用
class UserType(int, Enum):
    # VIP 用户
    VIP = 3
    # 黑名单用户
    BANNED = 13

# 用户每日奖励积分数量
DAILY_POINTS_REWARDS = 100
# VIP 用户每日额外奖励积分数量
VIP_EXTRA_POINTS = 20

def add_daily_points(user):
    """用户每天完成第一次登录后，为其增加积分"""
    if user.type == UserType.BANNED:
        return
    if user.points == UserType.VIP:
        user.points += DAILY_POINTS_REWARDS + VIP_EXTRA_POINTS
        return
    user.points += DAILY_POINTS_REWARDS
    return


# 2.使用 sqlalchemy 模块，代替SQL语句拼接

def fetch_users_v2(
    conn,
    min_level=None,
    gender=None,
    has_membership=False,
    sort_field="created",
):
    """获取用户列表"""
    query = select([users.c.id, users.c.name])
    if min_level != None:
        query = query.where(users.c.level >= min_level)
    if gender != None:
        query = query.where(users.c.gender == gender)
    query = query.where(users.c.has_membership == has_membership).order_by(users.c[sort_field])
    return list(conn.execute(query))


# 3.使用 Jinja2 模板处理字符串

# from jinja2 import Template

_MOVIES_TMPL = '''\
Welcome, {{username}}.
{%for name, rating in movies %}
* {{ name }}, Rating: {{ rating|default("[NOT RATED]", True)
}}
{%- endfor %}
'''

def render_movies_j2(username, movies):
    tmpl = Template(_MOVIES_TMPL)
    return tmpl.render(username=username, movies=movies)


# 4.使用特殊数字：“无穷大” 排序

def sort_users_inf(users):
    def key_func(username):
        age = users[username]
        # 当年龄为空时，返回正无穷大作为 key，因此就会被排到最后
        return age if age is not None else float('inf')
    return sorted(users.keys(), key=key_func)


# 4.改善超长字符串的可读性

s = ("This is the first line of a long string, "
"this is the second line")

s = "This is the first line of a long string, " \
"this is the second line"


# 5.多级缩进里出现多行字符串

from textwrap import dedent

message = dedent("""\
Welcome, today's movie list:
    - Jaw (1975)
    - The Shining (1980)
    - Saw (2004)""")

