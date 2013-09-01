# !/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth import models as auth_models

import time
from datetime import datetime

"""attribute in User
username(*), first_name, last_name, email, password, is_staff, is_active,
is_superuser, last_login, date_joined
"""
class Account(models.Model):

    w_uid = models.BigIntegerField(db_index=True, unique=True)
    w_name = models.CharField(max_length=100, blank=True)
    w_province = models.IntegerField(default=0, blank=True)
    w_city = models.IntegerField(default=0, blank=True)
    w_location = models.CharField(max_length=1000, blank=True)
    w_url = models.CharField(max_length=1000, blank=True)
    w_description = models.CharField(max_length=1000, blank=True)
    w_profile_image = models.CharField(max_length=500, blank=True) #用户头像地址，50×50像素
    w_gender = models.CharField(max_length=10, blank=True) #性别，m：男、f：女、n：未知
    w_followers_count = models.IntegerField(default=0)
    w_friends_count = models.IntegerField(default=0)
    w_statuses_count = models.IntegerField(default=0)
    w_favourites_count = models.IntegerField(default=0)
    w_bi_followers_count = models.IntegerField(default=0) #用户的互粉数
    w_created_at = models.DateTimeField(default=datetime.now, db_index=True)
    w_verified = models.BooleanField(default=False)
    
    feature = models.CharField(max_length=1000, blank=True)
    predict_category  =  models.IntegerField(default=0, blank=True) #default:0
    real_category  =  models.IntegerField(default=0, blank=True) #default:0
    
    fetched_at = models.DateTimeField(default=datetime.now, db_index=True)
    user = models.ForeignKey(auth_models.User, null=True, on_delete=models.CASCADE) #绑定系统用户，可选
    oauth = models.ForeignKey("UserOauth2", null=True, on_delete=models.CASCADE)
   

    def __unicode__(self):
        return u'{type:Account, w_name:%s}' % (self.w_name);
       
    @staticmethod
    def get_account(user):
        return Account.objects.get(user=user)

class UserOauth2(models.Model):

    w_uid = models.BigIntegerField(db_index=True, unique=True)
    access_token = models.CharField(max_length=100)
    expires_in = models.CharField(max_length=100)

    def is_expired(self):
        return float(self.expires_in) < time.time()

    def __unicode__(self):
        return u'{type:UserOauth2, w_uid:%s, is_expired:%s}' % \
            (self.w_id, self.is_expired())

