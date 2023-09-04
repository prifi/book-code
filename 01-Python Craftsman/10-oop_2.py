# -*- coding:utf-8 -*-

"""
@author: fly
@Created on: 2023/09/04 15:44
@Description: 
"""
from urllib import parse

"""
SOLID
    SRP：单一职责原则
    OCP：开放–关闭原则

SRP：单一职责原则
    - 一个类只应该有一种被修改的原因 ---大类拆分小类
    - 频繁修改，导致不同功能之间互相影响  ---逃避God Class

OCP：开放–关闭原则
    - 类应该对扩展(行为)开放，对修改封闭 ---继承、依赖注入和数据驱动
        sorted(l, key=lambda i: i % 3)
    - 继承：找到父类中不稳定、会变动的内容。将这部分变化封装成方法（或属性），子类才能通过继承重写这部分行为
        GithubOnlyHNTopPostsSpider()
    - 依赖注入：依赖注入抽离的通常是类
        HNTopPostsSpider(post_filter=GithubPostFilter()) 
    - 数据驱动：数据驱动抽离的是纯粹的数据，它的可定制性不如上面两种方式（假设新需求：保留以 .net 结尾过滤）
        hosts = ['github.com']
        HNTopPostsSpider(filter_by_hosts=hosts)
"""

# 1.SRP：单一职责原则
#
# 案例：Hacker News 新闻抓取脚本

import io
import sys
from typing import Iterable, TextIO, List, Optional

import requests
from lxml import etree

class Post:
    """Hacker News 上的条目

    :param title: 标题
    :param link: 链接
    :param points: 当前得分
    :param comments_cnt: 评论数
    """

    def __init__(self, title: str, link: str, points: str, comments_cnt: str):
        self.title = title
        self.link = link
        self.points = points
        self.comments_cnt = comments_cnt


class HNTopPostsSpider:
    """抓取 Hacker News Top 内容条目

    :param fp: 存储抓取结果的目标文件对象
    :param limit: 限制条目数，默认为 5
    """

    items_url = 'https://news.ycombinator.com/'
    file_title = 'Top news on HN'

    def __init__(self, fp: TextIO, limit: int = 5):
        self.fp = fp
        self.limit = limit

    def write_to_file(self):
        """以纯文本格式将 Hacker News Top 内容写入文件"""
        self.fp.write(f'# {self.file_title}\n\n')
        for i, post in enumerate(self.fetch(), 1):
            self.fp.write(f'> TOP {i}: {post.title}\n')
            self.fp.write(f'> 分数：{post.points} 评论数：{post.comments_cnt}\n')
            self.fp.write(f'> 地址：{post.link}\n')
            self.fp.write('------\n')

    def fetch(self) -> Iterable[Post]:
        """从 Hacker New 抓取 Top 内容

        :return: 可迭代的 Post 对象
        """
        resp = requests.get(self.items_url)
        html = etree.HTML(resp.text)
        items = html.xpath('//table//tr[@class="athing"]')
        for item in items[: self.limit]:
            node_title = item.xpath('./td[@class="title"]/span/a')[0]
            node_detail = item.getnext()  # 获取下一个兄弟 tr 节点
            points_text = node_detail.xpath('.//span[@class="score"]/text()')
            commnets_text = node_detail.xpath('.//td/span/a[last()]/text()')[0]
            yield Post(
                title=node_title.text,
                link=node_title.get('href'),
                points=points_text[0].split()[0] if points_text else '0',
                comments_cnt=commnets_text.split()[0]
            )

"""
# 执行：
crawler = HNTopPostsSpeder(sys.stdout)  # 写到控制台
crawler.write_to_file()

# 优化：拆分“抓取帖子列表”和“将帖子列表写入文件”两种职责类
"""


# OCP：开放–关闭原则
#
# 案例：支持过滤关注域名（如: github.com）

class PostsWriter:
    """负责将帖子列表写入文件中"""

    def __init__(self, fp: io.TextIOBase, title: str):
        self.fp = fp
        self.title = title

    def write(self, posts: List[Post]):
        self.fp.write(f'# {self.title}\n\n')
        for i, post in enumerate(posts, 1):
            self.fp.write(f'> TOP {i}: {post.title}\n')
            self.fp.write(f'> 分数：{post.points} 评论数：{post.comments_cnt}\n')
            self.fp.write(f'> 地址：{post.link}\n')
            self.fp.write('------\n')


# a.继承：通过继承改造

class HNTopPostsSpider:
    """抓取 Hacker News Top 内容条目

    :param limit: 限制条目数，默认为 5
    """

    items_url = 'https://news.ycombinator.com/'
    file_title = 'Top news on HN'

    def __init__(self, limit: int = 5):
        self.limit = limit

    def fetch(self) -> Iterable[Post]:
        """从 Hacker New 抓取 Top 内容

        :return: 可迭代的 Post 对象
        """
        counter = 0
        resp = requests.get(self.items_url)
        html = etree.HTML(resp.text)
        items = html.xpath('//table//tr[@class="athing"]')
        for item in items:
            if counter >= self.limit:
                break
            node_title = item.xpath('./td[@class="title"]/span/a')[0]
            node_detail = item.getnext()  # 获取下一个兄弟 tr 节点
            points_text = node_detail.xpath('.//span[@class="score"]/text()')
            commnets_text = node_detail.xpath('.//td/span/a[last()]/text()')[0]

            # 案例：只关注 GitHhub 内容
            # node_link = node_title.get('href')
            # parsed_link = parse.urlparse(node_link)
            # if parsed_link.netloc == 'github.com':
            #     counter += 1
            #     yield Post(
            #         title=node_title.text,
            #         link=parsed_link,
            #         points=points_text[0].split()[0] if points_text else '0',
            #         comments_cnt=commnets_text.split()[0]
            #     )

            post = Post(
                title=node_title.text,
                link=node_title.get('href'),
                points=points_text[0].split()[0] if points_text else '0',
                comments_cnt=commnets_text.split()[0]
            )

            if self.interested_in_post(post):
                counter += 1
                yield post

    # 需要被继承修改
    def interested_in_post(self, post: Post) -> bool:
        """判断是否应该将帖子加入结果集中"""
        return True

# 创建过滤子类
class GithubOnlyHNTopPostsSpider(HNTopPostsSpider):
    """只关心来自 GitHub 的内容"""

    def interested_in_post(self, post: Post) -> bool:
        parsed_link = parse.urlparse(post.link)
        return parsed_link.netloc == 'github.com'

# 执行
def get_hn_top_posts(fp: Optional[TextIO] = None):
    """获取 Hacker News Top 内容，并将其写入文件中
    :param fp: 需要写入的文件，如未提供，将向标准输出打印
    """
    dest_fp = fp or sys.stdout
    # crawler = HNTopPostsSpider()
    crawler = GithubOnlyHNTopPostsSpider()  # a.继承新的子类
    writer = PostsWriter(dest_fp, title='Top news on HN')
    writer.write(list(crawler.fetch()))

get_hn_top_posts()


# b.依赖注入：创建过滤类
class DefaultPostFilter:
    """默认保留所有帖子"""

    def validate(self, post: Post) -> bool:
        return True

class GithubPostFilter:
    """保留 Github 帖子"""

    def validate(self, post: Post) -> bool:
        parsed_link = parse.urlparse(post.link)
        return parsed_link.netloc == 'github.com'

class HNTopPostsSpider:
    """抓取 Hacker News Top 内容条目
    :param limit: 限制条目数，默认为 5
    :param post_filter: 过滤结果条目的算法，默认保留所有
    """

    items_url = 'https://news.ycombinator.com/'

    def __init__(self, limit: int = 5, post_filter = None):
        self.limit = limit
        self.post_filter = post_filter or DefaultPostFilter()

    def fetch(self) -> Iterable[Post]:
        """从 Hacker New 抓取 Top 内容

        :return: 可迭代的 Post 对象
        """
        counter = 0
        resp = requests.get(self.items_url)
        html = etree.HTML(resp.text)
        items = html.xpath('//table//tr[@class="athing"]')
        for item in items:
            if counter >= self.limit:
                break
            node_title = item.xpath('./td[@class="title"]/span/a')[0]
            node_detail = item.getnext()  # 获取下一个兄弟 tr 节点
            points_text = node_detail.xpath('.//span[@class="score"]/text()')
            commnets_text = node_detail.xpath('.//td/span/a[last()]/text()')[0]
            post = Post(
                title=node_title.text,
                link=node_title.get('href'),
                points=points_text[0].split()[0] if points_text else '0',
                comments_cnt=commnets_text.split()[0]
            )
            # 重写依赖注入过滤器
            if self.post_filter.validate(post):
                counter += 1
                yield post

# 执行
crawler = HNTopPostsSpider()
crawler = HNTopPostsSpider(post_filter=GithubPostFilter())
