#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from registration.views import activate
from registration.views import register
from registration.forms import PassChangeForm

urlpatterns = patterns('',
                       # 用户注册配置
                       url(r'^register/$', register, name='registration_register'),
                       # 注册完成
                       url(r'^register/complete/$', direct_to_template, {'template': 'registration/registration_complete.html'},
                           name='registration_complete'),

                       # 注册关闭
                       url(r'^register/closed/$', direct_to_template, {'template': 'registration/registration_closed.html'},
                           name='registration_disallowed'),

                       # 完成激活,这个配置必须在激活地址之前，否则永远匹配不到这儿来
                       url(r'^activate/complete/$', direct_to_template, {'template': 'registration/activation_complete.html'},
                           name='registration_activation_complete'),

                       # 用户激活码地址
                       # 使用 \w+ 而不使用精确的 [a-fA-F0-9]{40} 来匹配，因为当错误的时候提示用户
                       url(r'^activate/(?P<activation_key>\w+)/$', activate, name='registration_activate'),

                       # 用户登录
                       url(r'^login/$', auth_views.login,
                           {'template_name': 'registration/login.html'},
                           name='auth_login'),

                       # 注销
                       url(r'^logout/$', auth_views.logout,
                           {'template_name': 'registration/logout.html'},
                           name='auth_logout'),

                       # 改密码
                       url(r'^password/change/$', auth_views.password_change,
                           {'template_name': 'passwd/change_password.html',
                            'password_change_form': PassChangeForm,
                            },
                           name='auth_password_change'),

                       # 完成更改密码
                       url(r'^password/change/done/$', auth_views.password_change_done,
                           {'template_name': 'passwd/change_done.html'},
                           name='auth_password_change_done'),
                       )
