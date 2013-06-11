#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from forum.models import Forum, Thread, Post

class ForumAdmin(admin.ModelAdmin):
    list_display = ('title','slug','description','ordering', '_parents_repr')
    list_filter = ('groups',)
    ordering = ['ordering', 'parent', 'title']

    # 预定义输出，即title里面输入什么, slug默认就有什么,在英文输入状态下有效
    prepopulated_fields = {"slug": ("title",)}

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'sticky', 'closed', 'forum', 'latest_post_time')
    list_filter = ('forum',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author','thread','body')


admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
