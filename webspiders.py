#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/10/18
import base64
import random

import requests
from lxml import etree


class WanfangSpider(object):
    @classmethod
    def crawl_with_keyword(cls, keyword):
        url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=' + keyword
        print url
        response = requests.get(url, cls.get_headers())
        if response.status_code == 200:
            return cls.get_info(response.text)
        else:
            return None

    @classmethod
    def get_headers(cls):
        user_agent = [
            'Mozilla / 5.0(compatible;MSIE9.0;Windows NT 6.1;Trident / 5.0',
            'Mozilla / 4.0(compatible;MSIE6.0;Windows NT 5.1',
            'Mozilla / 5.0(compatible;MSIE7.0;Windows NT 5.1',
            'Mozilla / 5.0(compatible;MSIE8.0;Windows NT 6.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        ]
        headers = {
            'User-Agent': random.choice(user_agent)
        }
        return headers

    @classmethod
    def get_info(cls, content):
        tree = etree.HTML(content)
        divs = tree.xpath('//*[@class="left-record"]')
        result = []
        for div in divs:
            a_dict = {}
            url = div.xpath('div/a[@class="title"]/@href')
            title = div.xpath('div/a[@class="title"]')[0].xpath('string(.)')
            subtitle = div.xpath('div[@class="record-subtitle"]')[0].xpath('string(.)')
            # print url, title, subtitle
            if not title:
                title = None

            if url:
                url = url[0]
            else:
                url = None

            if subtitle:
                subtitle = subtitle.strip()
            else:
                subtitle = None
            a_dict['url'] = url
            a_dict['title'] = title
            a_dict['subtitle'] = subtitle
            result.append(a_dict)
        return result


class It199Spider(object):
    @classmethod
    def crawl_with_keyword(cls, keyword):
        url = 'http://www.199it.com/archives/tag/' + keyword
        print url
        proxies = {'http': 'http://332011270:omrdwhvf@120.76.130.77:16816/'}
        response = requests.get(url=url, proxies=proxies, headers=cls.get_headers())
        if response.status_code == 200:
            return cls.get_info(response.text)
        else:
            return None

    @classmethod
    def get_headers(cls):
        user_agent = [
            'Mozilla / 5.0(compatible;MSIE9.0;Windows NT 6.1;Trident / 5.0',
            'Mozilla / 4.0(compatible;MSIE6.0;Windows NT 5.1',
            'Mozilla / 5.0(compatible;MSIE7.0;Windows NT 5.1',
            'Mozilla / 5.0(compatible;MSIE8.0;Windows NT 6.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        ]
        headers = {
            'User-Agent': random.choice(user_agent)
        }
        return headers

    @classmethod
    def get_info(cls, content):
        tree = etree.HTML(content)
        articles = tree.xpath('//article')
        result = []
        for article in articles:
            a_dict = {}

            # 提取正文
            img_url = article.xpath('div[@class="entry-list-left"]/div/a/img/@src')
            title = article.xpath('div[@class="entry-list-right"]/h2/a/text()')
            url = article.xpath('div[@class="entry-list-right"]/h2/a/@href')
            post_time = article.xpath('div[@class="entry-list-right"]/table/tr/td[2]/text()')
            tag = article.xpath('div[@class="entry-list-right"]/table/tr/td[4]/a/text()')
            summary = article.xpath('div[@class="entry-list-right"]/p[@class="post-excerpt"]/text()')
            print img_url, url, title, post_time, tag, summary

            # 构造字典
            a_dict['img_url'] = img_url[0] if img_url else None
            a_dict['title'] = title[0] if title else None
            a_dict['url'] = url[0] if url else None
            a_dict['post_time'] = post_time[0] if post_time else None
            a_dict['tag'] = tag[0] if tag else None
            a_dict['summary'] = summary[0] if summary else None
            result.append(a_dict)
        return result if len(result) < 10 else result[0: 10]

    @classmethod
    def get_tags(cls, content):
        tree = etree.HTML(content)
        a_tags = tree.xpath('//div[@class="tagcloud"]/a')
        for a_tag in a_tags:
            tag = a_tag.xpath('text')


    @classmethod
    def get_content(cls, url):
        url = base64.decodestring(url)
        print url
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            tree = etree.HTML(content)
            # 标题
            title = tree.xpath('//h1[@class="entry-title"]/text()')
            post_time = tree.xpath('//*[@class="search-post-info-table"]/tr/td[2]/text()')
            entry_content = tree.xpath('//div[@class="entry-content"]')

            entry_content = etree.tostring(entry_content[0], pretty_print=True, )
            print entry_content
            obj =  {
                'msg': 'ok',
                'data': {'title': title[0] if title else None, 'post_time': post_time[0] if post_time else None, 'content': entry_content}
            }
        else:
            obj = {
                'msg': 'error',
                'data': {}
            }
        return obj

if __name__ == '__main__':
    It199Spider.get_content(url='http://www.199it.com/archives/532400.html')