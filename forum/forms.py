#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms


class ReplyForm(forms.Form):
    body = forms.CharField(label="内容",
                           min_length = 10,
                           error_messages = {'required':"请输入发表内容！",
                                             'min_length':"输入内容少于8个字符！"},
                           widget=forms.Textarea(attrs={'rows':10, 'cols':160}))


class CreateThreadForm(ReplyForm):
    """用户新建帖子，继承于回复帖子
    """
    title = forms.CharField(label="标题",
                            min_length=5,
                            max_length=100,
                            error_messages = {'required':"请输入标题！",
                                              'min_length':"输入内容少于5个字符！",
                                              'max_length':"输入内容大于100个字符！"},
                            )

# 字段的排序
CreateThreadForm.base_fields.keyOrder = ['title','body']
