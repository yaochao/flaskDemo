#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/10/18
import random
import urllib

import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


proxies = {'http': 'http://332011270:omrdwhvf@123.56.144.1:16816/'}

class WanfangSpider(object):
    @classmethod
    def crawl_with_keyword(cls, keyword):
        url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=' + urllib.quote(keyword)
        print url
        # response = requests.get(url=url, proxies=proxies, headers=cls.get_headers())
        response = requests.get(url=url, headers=cls.get_headers())
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
        divs = tree.xpath('//*[@class="record-item"]')
        # 如果结果为空那么就返回ggsimida
        if not divs:
            return 'ggsimida'
        # 不为空继续
        result = []
        for div in divs:
            a_dict = {}
            # url = div.xpath('div/a[@class="title"]/@href')
            url = div.xpath('div[@class="record-action-link"]/a[@class="view"]/@href')
            title = div.xpath('div/div/a[@class="title"]')[0].xpath('string(.)')
            subtitle = div.xpath('div/div[@class="record-subtitle"]')[0].xpath('string(.)')
            summary = div.xpath('div/div[@class="record-desc"]')
            if summary:
                summary = div.xpath('div/div[@class="record-desc"]')[0].xpath('string(.)')
            else:
                summary = ''
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
            if summary:
                summary = summary.strip()
            a_dict['url'] = url
            a_dict['title'] = title
            a_dict['subtitle'] = subtitle
            a_dict['summary'] = summary
            result.append(a_dict)
        return result


class It199Spider(object):
    @classmethod
    def crawl_with_keyword(cls, keyword):
        if keyword.strip() == '':
            return None
        url = 'http://s.199it.com/cse/search?s=913566115233094367&entry=1&q=' + urllib.quote(keyword)
        print url
        # response = requests.get(url=url, proxies=proxies, headers=cls.get_headers())
        response = requests.get(url=url, headers=cls.get_headers())
        if response.status_code == 200:
            return cls.get_info(response.content, keyword)
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
    def get_info(cls, content, keyword):
        tree = etree.HTML(content)
        results = tree.xpath('//div[@class="result f s0"]')
        # 如果结果为空那么就返回ggsimida
        if not results:
            return 'ggsimida'
        resultsss = []
        for result in results:
            a_dict = {}

            # 提取正文

            title = result.xpath('h3[@class="c-title"]/a')[0].xpath('string(.)')
            url = result.xpath('h3[@class="c-title"]/a/@href')

            c_abstract_image = result.xpath('div/div[@class="c-abstract-image"]')
            if c_abstract_image:
                summary = c_abstract_image[0].xpath('div[@class="c-abstract"]')[0].xpath('string(.)')
                img_url = result.xpath('div/div[@class="c-image page-pic"]/table/tr/td/img/@src')[0]
                post_time = result.xpath('div/div[2]/div[2]/span/text()')[0].split()[-1]
                if post_time and post_time[0].strip():
                    post_time = post_time[0].split()[-1]
            else:
                summary = result.xpath('div/div/div[@class="c-abstract"]')[0].xpath('string(.)')
                img_url = '/images/default.jpeg'
                post_time = result.xpath('div/div/div[2]/span/text()')
                if post_time and post_time[0].strip():
                    post_time = post_time[0].split()[-1]

            # 构造字典
            a_dict['img_url'] = img_url
            a_dict['title'] = title
            a_dict['url'] = url[0] if url else None
            a_dict['post_time'] = post_time
            a_dict['tag'] = keyword
            a_dict['summary'] = summary

            # 如果url链接的内容是列表就不加入resultsss
            if cls.is_list(a_dict['url']):
                resultsss.append(a_dict)
        return resultsss


    @classmethod
    def is_list(cls, url):
        '''
        如果含有.html则代表不是列表
        :param url:
        :return: True: 不是列表, False 是列表
        '''
        if '.html' in url:
            return True
        else:
            return False


if __name__ == '__main__':
    result = It199Spider.crawl_with_keyword('思密达')
    print len(result)
