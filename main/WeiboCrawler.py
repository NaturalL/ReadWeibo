# !/usr/bin/python
# -*- coding: utf-8 -*-

'''
Weibo Crawler

Created on Aug 29, 2013
@author: plex
'''
from main import Config
from libweibo import weibo
wclient = weibo.APIClient(app_key=Config.weibo_app_key,
                    app_secret = Config.weibo_app_secret,
                    redirect_uri = Config.callback_url)

from ReadWeibo.account.models import Account
from ReadWeibo.mainapp.models import Weibo
from datetime import datetime
from time import sleep

def CrawleHomeTimeline(w_uid, append=True, max_id=0, max_count=10000):
    '''
        更新用户的时间线上的微薄
    '''
    user = Account.objects.get(w_uid=w_uid)

    if user.oauth.is_expired():
        print 'WeiboUser:%s OAuth Expired' % user.w_name
        return
    else:
        wclient.set_access_token(user.oauth.access_token, user.oauth.expires_in)

    if append and user.weibo_set.count():
        since_wid = user.weibo_set.all()[0]
    else:
        since_wid = 0

    tot_fetched = 0
    page_size = 100
    page_id = 1
    while True:
        statuses = wclient.get.statuses__home_timeline(uid=w_uid,
                                            since_id=since_wid,
                                            max_id = max_id,
                                            count=page_size,
                                            page=page_id)[u'statuses']
        if statuses:

            #Store weibo
            for status in statuses:
#                 for key in status:
#                     print key, status[key]

                wb, created = Weibo.objects.get_or_create(w_id=status[u'id'])

                if created:
                    wb.created_at = datetime.strptime(status[u'created_at'],
                                                      "%a %b %d %H:%M:%S +0800 %Y")
                    wb.w_uid = status[u'user'][u'id']
                    wb.text = status[u'text']
                    wb.source = status[u'source']

                    if u'thumbnail_pic' in status:
                        wb.thumbnail_pic = status[u'thumbnail_pic']
                    if u'bmiddle_pic' in status:
                        wb.bmiddle_pic = status[u'bmiddle_pic']
                    if u'original_pic' in status:
                        wb.original_pic = status[u'original_pic']


                wb.reposts_count = status[u'reposts_count']
                wb.comments_count = status[u'comments_count']
                wb.attitudes_count = status[u'attitudes_count']

                wb.watcher.add(user)
                wb.save()

            tot_fetched += len(statuses)
            if tot_fetched >= max_count:
                break
        else:
            break

        print '%s - fetched %d status' % (datetime.now(), tot_fetched)
        page_id += 1
        sleep(0.5)

if __name__ == '__main__':
#     CrawleHomeTimeline(1698863684, append=False, max_id=3443452434246559)
    CrawleHomeTimeline(1698863684)
