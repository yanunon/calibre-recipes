#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-06-30 13:27

@author: Yang Junyong <yanunon@gmail.com>
'''
import urllib2
import json

from calibre.web.feeds.news import BasicNewsRecipe

USER_AGENT = 'ZhihuApi/1.0.0-beta (Linux; Android 4.2.2; Galaxy Nexus Build/Google/yakju/maguro/JDQ39/zh_CN) Google-HTTP-Java-Client/1.15.0-rc (gzip) Google-HTTP-Java-Client/1.15.0-rc (gzip)'
HEADER = {'User-Agent' : USER_AGENT}
LATEST_URL = 'http://daily.zhihu.com/api/1.2/news/latest'

class ZhihuDailyRecipe(BasicNewsRecipe):
    title = u'知乎日报'
    auto_cleanup = True
    no_stylesheets = True
    #simultaneous_downloads = 10
    delay = 1.0
    timeout = 5
    timefmt = '[%Y %m %d]'

    def get_browser(self, *args, **kwargs):
        from calibre import browser
        kwargs['user_agent'] = USER_AGENT
        return browser(*args, **kwargs)

    def get_cover_url(self):
        return 'http://daily.zhihu.com/img/Logo.png'

    def parse_index(self):
        req = urllib2.Request(LATEST_URL, headers=HEADER)
        resp = urllib2.urlopen(req)
        newses = json.loads(resp.read())
        today = []

        for news in newses['news']:
            title = news['title'].encode('utf-8')
            url = news['share_url']
            date = newses['display_date'].encode('utf-8')
            today.append({
                'title': title,
                'url': url,
                'date': date,
                'description': '',
                'content': ''
                })

        top_story = []
        for story in newses['top_stories']:
            title = story['title'].encode('utf-8')
            url = story['share_url']
            date = newses['display_date'].encode('utf-8')
            top_story.append({
                'title': title,
                'url': url,
                'date': date,
                'description': '',
                'content': ''
                })

        return [('Today', today), ('Top Story', top_story)]

