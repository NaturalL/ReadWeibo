# !/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Oct 12, 2012

@author: plex
'''

from django.db import models

from ReadWeibo.account.models import Account
from datetime import datetime


class Weibo(models.Model):
    created_at = models.DateTimeField(default=datetime.now, db_index=True)
    w_id = models.BigIntegerField(unique=True, db_index=True)
    w_uid = models.BigIntegerField(blank=True, null=True) #owner
    text = models.CharField(max_length=500, blank=True)
    source = models.CharField(max_length=500, blank=True)
    thumbnail_pic = models.CharField(max_length=500, blank=True)
    bmiddle_pic = models.CharField(max_length=500, blank=True)
    original_pic = models.CharField(max_length=500, blank=True)
    reposts_count = models.IntegerField(default=0, blank=True)
    comments_count = models.IntegerField(default=0, blank=True)
    attitudes_count =  models.IntegerField(default=0, blank=True)
    
    watcher = models.ManyToManyField(Account, blank=True, null=True) # who can see this

    def __unicode__(self):
        return u'[Weibo , %d]' % self.w_id

    class Meta:
        ordering = ["-w_id"]