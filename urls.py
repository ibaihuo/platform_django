#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import include,patterns,url

from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

# urlpatterns为固定变量，是函数patterns的返回值
urlpatterns = patterns('',
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                    
    # 默认首页
    url(r'^$', 'team.views.notice'),
    url(r'^notice/(\d+)/$', 'team.views.notice_detail'),

    # 验证码
    url(r'^image/(?P<key>\w+)/$', 'captcha.views.captcha',name='captcha-image'),

    # account
    url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/profile/$', 'team.views.profile'),
    url(r'^accounts/profile/edit/$', 'team.views.profile_edit'),      
    url(r'^accounts/profile/edit_not_allowed/$',direct_to_template,{'template':'profile/edit_not_allowed.html'}),

    # Challenge
    url(r'^challenge/$', 'team.views.challenge',name="challenge_index"),
    url(r'^challenge/(\d+)/$','team.views.challenge_detail',name="challenge_detail"),
    url(r'^challenge/(\d+)/submit/$','team.views.submit_answer'),
    url(r'^challenge/submit-closed/$',direct_to_template,{'template':'challenge/submit-closed.html'}),

    # Challenge Choice                       
    url(r'^challenge/choice/$','team.views.challenge_choice'),                       
    url(r'^challenge/choice/(\d+)/$','team.views.challenge_choice_detail'),                       

    # 积分排名
    url(r'^rank/$','team.views.rank'),
    url(r'^rank/report/$','team.views.rank_report'),


    # 论坛配置
    url(r'^forum/', include('forum.urls')),

    # 关于界面，直接显示html
    url(r'^about/$',direct_to_template,{'template':'about.html'}),

    # 管理员登录入口，请修改这儿
    url(r'^admin/', include(admin.site.urls)),
)
