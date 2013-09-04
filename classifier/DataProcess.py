# !/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2013-9-2

@author: plex
'''
from ReadWeibo.mainapp.models import Weibo
from ReadWeibo.account.models import Account
from main.djangodb import WeiboDao
from datetime import datetime
from sets import Set
from mmseg import seg_txt
import numpy as np
import re

#TODO 去停用词 规范化单词
def generate_user_dict(w_uid):
	user = Account.objects.get(w_uid=w_uid)
	wbs = user.watchweibo.all()
	wordset = Set()
	
	print 'Generating user dict with %d weibo to deal with' % len(wbs)
	
	for wb in wbs:
		for word in seg_txt(wb.text.encode('utf-8','ignore')):
			if len(word)>3:
				wordset.add(word.lower().strip())

	with open("../data/user_dict/%s.dic" % w_uid, "w") as dic_file:
		for word in wordset:
			dic_file.write("%s\n" % word)

def load_dict(w_uid):
	dict = {}
	with open("../data/user_dict/%s.dic" % w_uid, "r") as dic_file:
		id = 0
		for word in dic_file:
			dict[word.strip().encode("utf-8", "ignore")] = id
			id += 1
	return dict

def generate_feature(wb, dict):
	fea = [0]*len(dict)
	# 微博文本
	for wd in seg_txt(wb.text.encode('utf-8','ignore')):
		word_count = 0
		wd = wd.lower().strip()
		if len(wd)>3 and wd in dict:
			fea[dict[wd]] += 1
			word_count += 1
		print 'found %d word in a weibo' % word_count

	# add user features
	owner = wb.owner
	fea.append(int(owner.w_province))
	fea.append(int(owner.w_city))
	if owner.w_url:
		fea.append(1)
	else:
		fea.append(0)
	fea.append(len(owner.w_description))
	if 'm' in owner.w_gender:
		fea.append(1)
	else:
		fea.append(0)

	fea.append(int(owner.w_followers_count))
	fea.append(int(owner.w_friends_count))
	fea.append(int(owner.w_statuses_count))
	fea.append(int(owner.w_favourites_count))
	fea.append(int(owner.w_bi_followers_count))
	fea.append((datetime.now()-owner.w_created_at).days/100)
	if owner.w_verified:
		fea.append(1)
	else:
		fea.append(0)


	# add weibo features
	fea.append(int(wb.reposts_count))
	fea.append(int(wb.comments_count))
	fea.append(int(wb.attitudes_count))
	if re.search("#.*?#", wb.text):
		fea.append(1)
	else:
		fea.append(0)

	fea.append(len(wb.text))
	own_text = re.search("(.*?)//@", wb.text)
	if own_text:
		fea.append(len(own_text.group(1)))
	else:
		fea.append(len(wb.text))
	#TODO 对source归类
	fea.append(len(wb.source))

	if wb.retweeted_status:
		fea.append(0)
	else:
		fea.append(1)

	if wb.thumbnail_pic:
		fea.append(1)
	else:
		fea.append(0)
	fea.append(wb.created_at.hour)
	fea.append(wb.created_at.weekday())
	# TODO 计算微博转发评论的衰减公式

	return fea

def generate_train_file(w_uid):
	
	print 'Generating train file for user %s' % w_uid
	
	user = Account.objects.get(w_uid=w_uid)
	wbs = user.watchweibo.filter(real_category__gt=0)
	word_dic = load_dict(w_uid)
	
	print 'Train set size:', len(wbs)
	
	with open("../data/training/%s.tr" % w_uid, "w") as train_file:
		for wb in wbs:
			for fea in generate_feature(wb, word_dic):
				train_file.write("%s\t" % fea)
				
			train_file.write("%s\n" % wb.real_category)

if __name__ == '__main__':
# 	generate_user_dict(1698863684)
	generate_train_file(1698863684)
# 	print generate_feature(Weibo.objects.get(w_id=3617663458268921),{})
	pass
