# !/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.utils import simplejson

from ReadWeibo.account.models import Account

from libweibo import weibo
from main import Config


import datetime
import itertools
import re

_DEBUG = True
_mimetype = u'application/javascript, charset=utf8'

wclient = weibo.APIClient(app_key=Config.weibo_app_key,
                    app_secret = Config.weibo_app_secret,
                    redirect_uri = Config.callback_url)
# wclient.set_access_token("2.00l9nr_DfUKrWDf655d3279arZgVvD", "1511349376")

def home(request):
    template_var = {}
    print 'current login user: ', request.user
    if request.user.is_authenticated() and not request.user.is_superuser:
#         template_var['cur_user'] = User.objects.get(username=request.user.username).account_set.all()[0]
        user = Account.objects.get(w_name=request.user.username)

        watch_weibo = user.watchweibo.exclude(bmiddle_pic__startswith='h')[:10]
        size = len(watch_weibo) / 2; print len(watch_weibo)
        template_var['watch_weibo_left'] = watch_weibo[:size]
        template_var['watch_weibo_right'] = watch_weibo[size:]
        template_var['cur_user'] = user
    else:
        template_var['authorize_url'] = wclient.get_authorize_url()

    return render_to_response("home.html", template_var,
                              context_instance=RequestContext(request))












