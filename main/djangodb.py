from ReadWeibo.account.models import Account
from ReadWeibo.mainapp.models import Weibo
from datetime import datetime

class WeiboDao:

    @staticmethod
    def create_or_update(weiboJson):
        status = weiboJson
        wb, created = Weibo.objects.get_or_create(w_id=status[u'id'])

        if created:
            if status[u'created_at']:
                wb.created_at = datetime.strptime(status[u'created_at'], "%a %b %d %H:%M:%S +0800 %Y")
            wb.text = status[u'text']

            if u'source' in status:
                wb.source = status[u'source']

            if u'thumbnail_pic' in status:
                wb.thumbnail_pic = status[u'thumbnail_pic']
            if u'bmiddle_pic' in status:
                wb.bmiddle_pic = status[u'bmiddle_pic']
            if u'original_pic' in status:
                wb.original_pic = status[u'original_pic']

            wb.owner = AccountDao.create_or_update(status[u'user'])

            if u'retweeted_status' in status:
                wb.retweeted_status = WeiboDao.create_or_update(status[u'retweeted_status'])
                wb.retweeted_status.watcher.add(wb.owner)


        wb.reposts_count = status[u'reposts_count']
        wb.comments_count = status[u'comments_count']
        wb.attitudes_count = status[u'attitudes_count']
        wb.fetched_at = datetime.now()
        wb.save()

        return wb

    @staticmethod
    def get_weibo(weiboJson):
        status = weiboJson
        wb, created = Weibo.objects.get_or_create(w_id=status[u'id'])

        if created:
            if status[u'created_at']:
                wb.created_at = datetime.strptime(status[u'created_at'], "%a %b %d %H:%M:%S +0800 %Y")
            wb.text = status[u'text']

            if u'source' in status:
                wb.source = status[u'source']

            if u'thumbnail_pic' in status:
                wb.thumbnail_pic = status[u'thumbnail_pic']
            if u'bmiddle_pic' in status:
                wb.bmiddle_pic = status[u'bmiddle_pic']
            if u'original_pic' in status:
                wb.original_pic = status[u'original_pic']

            wb.owner = AccountDao.create_or_update(status[u'user'])

            if u'retweeted_status' in status:
                wb.retweeted_status = WeiboDao.create_or_update(status[u'retweeted_status'])
                wb.retweeted_status.watcher.add(wb.owner)


        wb.reposts_count = status[u'reposts_count']
        wb.comments_count = status[u'comments_count']
        wb.attitudes_count = status[u'attitudes_count']
        wb.fetched_at = datetime.now()
        wb.save()

        return wb


class AccountDao:

    @staticmethod
    def create_or_update(weiboUserJson):

        uinfo=weiboUserJson
        account, created = Account.objects.get_or_create(w_uid=uinfo[u'id'])

        if created:
            account.w_name=uinfo['name']
            account.w_province=uinfo['province']
            account.w_city=uinfo['city']
            account.w_location=uinfo['location']
            account.w_url=uinfo['url']
            account.w_description=uinfo['description']
            account.w_profile_image=uinfo['profile_image_url']
            account.w_gender=uinfo['gender']
            account.w_created_at=datetime.strptime(uinfo['created_at'], "%a %b %d %H:%M:%S +0800 %Y")

        account.w_followers_count=uinfo['followers_count']
        account.w_friends_count=uinfo['friends_count']
        account.w_statuses_count=uinfo['statuses_count']
        account.w_favourites_count=uinfo['favourites_count']
        account.w_bi_followers_count=uinfo['bi_followers_count']
        account.w_verified=uinfo['verified']
        account.fetched_at=datetime.now()
        account.save()

        return account
