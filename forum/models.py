#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" 
论坛数据模型
"""

from django.db import models
import datetime
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.html import escape

try:
    from markdown import markdown
except ImportError:
    class MarkdownNotFound(Exception):
        def __str__(self):
            return "Markdown is not installed!"
    raise MarkdownNotFound

from forum.managers import ForumManager

class Forum(models.Model):
    """
    论坛版块
    """
    groups = models.ManyToManyField(Group,verbose_name="隶属组", blank=True)
    title = models.CharField("标题", max_length=100)
    slug = models.SlugField("地址", unique=True)     # 访问地址
    parent = models.ForeignKey('self',verbose_name="上级论坛", blank=True, null=True, related_name='child') # 上级话题
    description = models.TextField("介绍")
    threads = models.IntegerField("帖子数目", default=0, editable=False) # 帖子数目
    posts = models.IntegerField("回复数量", default=0, editable=False) # 回复数目
    ordering = models.IntegerField("排序", blank=True, null=True) # 当前版块的序号

    objects = ForumManager()

    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        ordering = ['ordering', 'title',] # 默认取数据与存储的排序
        # verbose_name = '论坛'

    def _get_forum_latest_post(self):
        """获取本论坛版块最后发表的帖子
        """
        if not hasattr(self, '__forum_latest_post'):
            try:
                self.__forum_latest_post = Post.objects.filter(thread__forum__pk=self.id).latest("time")
                # filter里面的下划线表示继续深入表（外键）
            except Post.DoesNotExist:
                self.__forum_latest_post = None

        return self.__forum_latest_post
    forum_latest_post = property(_get_forum_latest_post)

    def _recurse_for_parents_slug(self, forum_obj):
        """
        递归获得上级论坛的显示url（不完整）
        """
        p_list = []
        if forum_obj.parent_id:
            p = forum_obj.parent
            p_list.append(p.slug)
            more = self._recurse_for_parents_slug(p)
            p_list.extend(more)

        if forum_obj == self and p_list:
            p_list.reverse()

        return p_list

    def get_absolute_url(self):
        """获得完整的url路径
        """
        from django.core.urlresolvers import reverse
        p_list = self._recurse_for_parents_slug(self)
        p_list.append(self.slug)
        return '%s%s/' % (reverse('forum_index'), '/'.join (p_list))

    def _recurse_for_parents_name(self, forum_obj):
        """递归获取上级论坛的名字，
        用途：1、后台显示上级论坛
        2、验证是否当前论坛的上级论坛是自身
        """
        p_list = []
        if forum_obj.parent_id:
            p = forum_obj.parent
            p_list.append(p.title)
            more = self._recurse_for_parents_name(p)
            p_list.extend(more)
        if forum_obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        """返回一个分隔符
        """
        return ' &raquo; '

    def _parents_repr(self):
        """返回所有上级论坛的字符串表示
        """
        p_list = self._recurse_for_parents_name(self)
        return self.get_separator().join(p_list)
    _parents_repr.short_description = "上级论坛"

    def _recurse_for_parents_name_url(self, forum__obj):
        """获取所有上级论坛的绝对路径和名字
        """
        p_list = []
        url_list = []

        if forum__obj.parent_id:
            p = forum__obj.parent
            p_list.append(p.title)
            url_list.append(p.get_absolute_url())
            more, url = self._recurse_for_parents_name_url(p)
            p_list.extend(more)
            url_list.extend(url)
        if forum__obj == self and p_list:
            p_list.reverse()
            url_list.reverse()
        return p_list, url_list

    def get_url_name(self):
        """递归获取上级论坛及自身的名字，url地址
        用途：显示论坛导航地址及链接
        返回：一个相对应的两个元组组成的一个列表
        """
        p_list, url_list = self._recurse_for_parents_name_url(self)

        # 添加自身
        p_list.append(self.title)
        url_list.append(self.get_absolute_url())

        return zip(p_list, url_list)


    # def save(self, force_insert=False, force_update=False):
    #     p_list = self._recurse_for_parents_name(self)
    #     if (self.title) in p_list:
    #         raise validators.ValidationError(_("不能将自身设置为自身的上级论坛"))
    #     super(Forum, self).save(force_insert, force_update)

class Thread(models.Model):
    """
    帖子
    """
    forum = models.ForeignKey(Forum, verbose_name="隶属论坛")
    title = models.CharField("标题", max_length=100)
    sticky = models.BooleanField("置顶?", blank=True, default=False)
    closed = models.BooleanField("关闭?", blank=True, default=False)
    posts = models.IntegerField("回复数", default=0)
    views = models.IntegerField("点击量", default=0)
    latest_post_time = models.DateTimeField("最后发表", blank=True, null=True)

    class Meta:
        ordering = ('-sticky', '-latest_post_time')
        verbose_name = 'Thread'


    def _get_thread_latest_post(self):
        """获取本帖子的最后回复
        """
        if not hasattr(self, '__thread_latest_post'):
            try:
                self.__thread_latest_post = Post.objects.filter(thread__pk=self.id).latest("time")
            except Post.DoesNotExist:
                self.__thread_latest_post = None

        return self.__thread_latest_post
    thread_latest_post = property(_get_thread_latest_post)


    def save(self, force_insert=False, force_update=False):
        f = self.forum
        f.threads = f.thread_set.count()
        f.save()
        if not self.sticky:
            self.sticky = False
        super(Thread, self).save(force_insert, force_update)

    def delete(self):
        super(Thread, self).delete()
        f = self.forum
        f.threads = f.thread_set.count()
        f.posts = Post.objects.filter(thread__forum__pk=f.id).count()
        f.save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('view_thread', [str(self.id)])
    
    def __unicode__(self):
        return u'%s' % self.title

class Post(models.Model):
    """ 
    发表的内容
    """
    thread = models.ForeignKey(Thread,verbose_name="属于帖子")
    author = models.ForeignKey(User,verbose_name="作者", related_name='forum_post_set')
    body = models.TextField("内容")
    body_html = models.TextField(editable=False)
    time = models.DateTimeField("发布时间", blank=True, null=True)

    class Meta:
        ordering = ('-time',)
        verbose_name = 'Post'

    def __unicode__(self):
        return u"%s" % self.id


    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.time = datetime.datetime.now()
        
        self.body_html = markdown(escape(self.body))
        super(Post, self).save(force_insert, force_update)

        t = self.thread
        t.latest_post_time = t.post_set.latest('time').time
        t.posts = t.post_set.count()
        t.save()

        f = self.thread.forum
        f.threads = f.thread_set.count()
        f.posts = Post.objects.filter(thread__forum__pk=f.id).count()
        f.save()

    def delete(self):
        try:
            latest_post = Post.objects.exclude(pk=self.id).latest('time')
            latest_post_time = latest_post.time
        except Post.DoesNotExist:
            latest_post_time = None

        t = self.thread
        t.posts = t.post_set.exclude(pk=self.id).count()
        t.latest_post_time = latest_post_time
        t.save()

        f = self.thread.forum
        f.posts = Post.objects.filter(thread__forum__pk=f.id).exclude(pk=self.id).count()
        f.save()

        super(Post, self).delete()

    def get_absolute_url(self):
        return '%s?page=last#post%s' % (self.thread.get_absolute_url(), self.id)
