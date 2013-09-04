# !/usr/bin/python
# -*- coding: utf-8 -*-

'''
Weibo Crawler

Created on Aug 29, 2013
@author: plex
'''
from main import Config
from main.djangodb import AccountDao, WeiboDao
from libweibo import weibo
wclient = weibo.APIClient(app_key=Config.weibo_app_key,
                    app_secret = Config.weibo_app_secret,
                    redirect_uri = Config.callback_url)

from ReadWeibo.account.models import Account
from ReadWeibo.mainapp.models import Weibo
from datetime import datetime
from time import sleep
import traceback

def CrawleCommentsToUser(w_uid):
    # TODO
    pass

def CrawleCommentsFromUser(w_uid):
    # TODO
    pass

def CrawleMentionsToUser(w_uid):
    # TODO
    pass

def CrawleHomeTimeline(w_uid, append=True, max_id=0, max_count=2000):
    '''
        更新用户的时间线上的微薄
    '''
    user = Account.objects.get(w_uid=w_uid)
    if user.oauth.is_expired():
        print 'WeiboUser:%s OAuth Expired' % user.w_name
        return
    else:
        wclient.set_access_token(user.oauth.access_token, user.oauth.expires_in)

    print "%s - Start crawling %s's HomeTimeline" % (datetime.now(), user.w_name)

    if append and user.watchweibo.count():
        since_wid = user.watchweibo.all()[0].w_id
    else:
        since_wid = 0

    tot_fetched = 0
    page_size = 20 # fast the fist time
    page_id = 1
    while True:
        statuses = wclient.get.statuses__home_timeline(uid=w_uid,
                                            since_id=since_wid,
                                            max_id = max_id,
                                            count=page_size,
                                            page=page_id)[u'statuses']
        if statuses:
            for status in statuses:
                try:
                    weibo = WeiboDao.create_or_update(status)
                    weibo.watcher.add(user)
                    weibo.save()
                except Exception, e:
                    print status
                    print traceback.format_exc()
            tot_fetched += len(statuses)
            if tot_fetched >= max_count:
                break
        else:
            break
        page_size = 100
        print '%s - fetched %d status' % (datetime.now(), tot_fetched)
        page_id += 1
        sleep(0.5)

    print "%s - Crawling %s's HomeTimeline Over with %d new status" % (datetime.now(), user.w_name, tot_fetched)

if __name__ == '__main__':
#      CrawleHomeTimeline(1698863684, append=False, max_id=3616800669525985)
     CrawleHomeTimeline(1698863684, append=False)

