#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
用户注册和激活账号向导
"""

from team.conf import settings
from django.contrib.sites.models import Site,RequestSite

from registration.forms import RegistrationForm
from team.models import TeamProfile

from django.shortcuts import redirect,render_to_response
from django.template import RequestContext
from team.forms import ProfileForm

def register(request,
             disallowed_url='registration_disallowed',
             template_name='registration/registration.html'):
    """用户注册
    """

    # 是否允许用户进行注册
    allow_register = getattr(settings, 'REGISTRATION_OPEN', False)

    if not allow_register:
        return redirect(disallowed_url)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        # 数据验证
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']        

            # 创建一个未激活的用户和默认的扩展属性
            act_key = TeamProfile.objects.create_inactive_user(username, email, password)

            # 直接将激活码作为链接发给用户
            to, args, kwargs = ('registration_activate',(), {'activation_key':act_key})
            return redirect(to, *args, **kwargs)
    else:
        form = RegistrationForm()
    
    context = RequestContext(request)

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)

def activate(request, activation_key,
             template_name='registration/activate.html',
             **kwargs):
    """激活用户账号
    """

    profile = TeamProfile.objects.fake_activate_user(activation_key)

    context = RequestContext(request)

    if profile:
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)

            if form.is_valid():
                form.save()                 # 更新数据

                to, args, kwargs = ('registration_activation_complete', (), {})
                return redirect(to, *args, **kwargs)
        else:
            form = ProfileForm(instance=profile)
            return render_to_response('profile/profile_create.html',
                                      {'form':form},
                                      context_instance=context)

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)
