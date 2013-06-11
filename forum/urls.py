#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf.urls.defaults import *
from forum.models import Forum

urlpatterns = patterns('',
                       # 版块列表
                       url(r'^$', 'forum.views.forums_list', name='forum_index'), # 使用了命名的url Pattern

                       # 帖子列表
                       url(r'^thread/(?P<thread>\d+)/$', 'forum.views.thread', name='view_thread'),

                       # 回复帖子
                       url(r'^thread/(?P<thread>\d+)/reply/$', 'forum.views.reply', name='reply_thread'),

                       # 论坛地址
                       url(r'^(?P<slug>[-\w]+)/$', 'forum.views.forum', name='thread_list'),

                       # 一级论坛增加帖子
                       url(r'^(?P<forum>[-\w]+)/new/$', 'forum.views.newthread', name='new_thread'),

                       # 二级及以下论坛增加帖子
                       url(r'^([-\w/]+/)(?P<forum>[-\w]+)/new/$', 'forum.views.newthread'),

                       # 所有下级帖子   注： 这个应该在最后，否则会匹配前面的规则
                       url(r'^([-\w/]+/)(?P<slug>[-\w]+)/$', 'forum.views.forum', name='subforum_thread_list'),
                       )
