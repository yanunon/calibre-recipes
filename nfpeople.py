#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-07-04 23:06

@author: Yang Junyong <yanunon@gmail.com>
'''
import urllib2
import json
import time
from datetime import datetime, timedelta
from calibre.web.feeds.news import BasicNewsRecipe

SA = {
        'toutiao': '头条',
        'fengmian': '封面',
        'xinwen': '新闻',
        'shangye': '商业',
        'wenhua': '文化',
        'tiyu': '体育',
        'yule': '娱乐',
    }

def get_article_url(id):
    return 'http://nfrwzk.cms.palmtrends.com/api_v2.php?action=article&id=%d&mode=day&uid=1234567' % (id)

def get_article(sa, from_time):
    url = 'http://nfrwzk.cms.palmtrends.com/api_v2.php?action=list&sa=%s&offset=0&count=20&uid=1234567' % (sa)
    resp = urllib2.urlopen(url)
    data = json.loads(resp.read())
    article = []
    for item in data['list']:
        t = datetime.fromtimestamp(int(item['timestamp']))
        if t > from_time:
            if sa == 'fengmian':
                time.sleep(5)
                url = 'http://nfrwzk.cms.palmtrends.com/api_v2.php?action=cover&sa=fengmians&id=%d&offset=0&count=10&uid=1234567' % (int(item['id']))
                resp = urllib2.urlopen(url)
                cover_data = json.loads(resp.read())
                if cover_data['code'] == 1:
                    for cover_item in cover_data['list']:
                        article.append([int(cover_item['id']), cover_item['title']])
            else:
                article.append([int(item['id']), item['title']])
    return article

def get_weekly():
    now = datetime.now()
    from_time = now - timedelta(days=7)
    articles = {}
    exist_id = []
    for sa in SA.keys():
        article = get_article(sa, from_time)
        
        for item in article:
            if item[0] in exist_id:
                article.remove(item)
            else:
                exist_id.append(item[0])

        articles[SA[sa]] = article
        time.sleep(5)

    return articles

class NanFangPeopleRecipe(BasicNewsRecipe):
    title = u'南方人物周刊'
    auto_cleanup = True
    no_stylesheets = True
    timeout = 5
    timefmt = ' [%Y %m %d]'
    remove_tags = [dict(id='o_info')]

    def parse_index(self):
        self.title += datetime.now().strftime(self.timefmt)
        articles = get_weekly() 
        index = []
        for a in articles.keys():
            if len(articles[a]) < 1:
                continue
            
            story = []
            for item in articles[a]:
                title = item[1]
                url = get_article_url(item[0])
                story.append({
                    'title': title,
                    'url': url,
                    'date': '',
                    'description': '',
                    'content': ''})
            index.append((a, story))
        return index

    def get_cover_url(self):
        return 'http://www.nfpeople.com/FrontApp/Tpl/default/Public/Images/logo.jpg'

if __name__ == '__main__':
    get_weekly()
