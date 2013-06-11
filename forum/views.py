#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from django.template import RequestContext, Context, loader
from django import forms

from team.conf import settings
from django.template.defaultfilters import striptags, wordwrap
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list


from forum.models import Forum,Thread,Post
from forum.forms import CreateThreadForm, ReplyForm

FORUM_PER_PAGE = getattr(settings, 'FORUM_PER_PAGE', 10)


def forums_list(request):
    """列出所有的一级论坛
    """
    # 获取当前用户属于的所有组
    the_groups = request.user.groups.all()
    #print the_groups

    queryset = Forum.objects.for_groups(the_groups).filter(parent__isnull=True)
    # print queryset

    # 调用通用视图，使用app/object.html(forum/forums_list.html)来渲染
    return object_list(request,
                        queryset=queryset)

@login_required
def forum(request, slug):
    """
    显示当前论坛下面的帖子数
    select_related()增加了缓存性能
    """
    the_groups = request.user.groups.all()


    # 防止直接输入不存在或者没有权限的地址进行访问
    try:
        f = Forum.objects.for_groups(the_groups).select_related().get(slug=slug)
    except Forum.DoesNotExist:
        raise Http404

    form = CreateThreadForm()
    child_forums = f.child.for_groups(the_groups)
    return object_list( request,
                        queryset=f.thread_set.select_related().all(),
                        paginate_by=FORUM_PER_PAGE,
                        template_object_name='thread',
                        template_name='forum/thread_list.html',
                        extra_context = {
                            'forum': f,
                            'child_forums': child_forums,
                            'form': form,
                        })

@login_required
def thread(request, thread):
    """
    增加帖子子的点击数
    并显示本帖子里发布的话题
    """
    try:
        t = Thread.objects.select_related().get(pk=thread)
        if not Forum.objects.has_access(t.forum, request.user.groups.all()):
            raise Http404
    except Thread.DoesNotExist:
        raise Http404

    p = t.post_set.select_related('author').all().order_by('time')

    # 增加帖子的访问量
    t.views += 1
    t.save()

    form = ReplyForm()

    return object_list( request,
                        queryset=p,
                        paginate_by=FORUM_PER_PAGE,
                        template_object_name='post',
                        template_name='forum/thread.html',
                        extra_context = {
                            'forum': t.forum,
                            'thread': t,
                            'form': form,
                        })

@login_required
def reply(request, thread):
    """
    回复帖子子
    条件：
    1、帖子允许回复，没有关闭
    2、当前用户登录
    """
    t = get_object_or_404(Thread, pk=thread)
    if t.closed:
        return Http404
    if not Forum.objects.has_access(t.forum, request.user.groups.all()):
        return Http404

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            p = Post(
                thread=t, 
                author=request.user,
                body=body,
                time=datetime.now(),
                )
            p.save()

            return HttpResponseRedirect(p.get_absolute_url())
    else:
        form = ReplyForm()

    return render_to_response('forum/reply.html',
                              RequestContext(request, {'form': form,
                                                       'forum': t.forum,
                                                       'thread': t,
                                                       }))

@login_required
def newthread(request, forum):
    """
    新建帖子
    """
    f = get_object_or_404(Forum, slug=forum)

    if not Forum.objects.has_access(f, request.user.groups.all()):
        return Http404

    if request.method == 'POST':
        form = CreateThreadForm(request.POST)
        if form.is_valid():
            t = Thread(
                forum=f,
                title=form.cleaned_data['title'],
            )
            t.save()

            p = Post(
                thread=t,
                author=request.user,
                body=form.cleaned_data['body'],
                time=datetime.now(),
            )
            p.save()

            return HttpResponseRedirect(t.get_absolute_url())
    else:
        form = CreateThreadForm()

    return render_to_response('forum/newthread.html',
                              RequestContext(request, {'form': form,
                                                       'forum': f,
                                                       }))
