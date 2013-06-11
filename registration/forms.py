#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField
import string

class RegistrationForm(forms.Form):
    """用户注册表单
    """
    username = forms.RegexField(regex=r'^\w+$',
                                min_length = 3, # 最小长度为3字符，
                                max_length = 8, # 最大长度为8
                                widget=forms.TextInput(),
                                label="登录ID",

                                error_messages={'required': "登录ID不能为空!",
                                                'min_length': "登录ID最少包含3个字符!",
                                                'max_length': "登录ID最多包含8个字符!",
                                                'invalid': "登录ID只能包含:字母，数字和下划线!"
                                                }
                                )

    email = forms.EmailField(widget=forms.TextInput(),
                             min_length = 10,
                             max_length = 20,
                             label="邮箱",
                             help_text="如果需要的话，会用此邮箱联系你们！",
                             error_messages={'required': "请填写有效的邮箱！",
                                             'invalid':"请输入合法且有效的邮件地址!",
                                             'min_length': "邮箱最少包含10个字符!",
                                             'max_length': "邮箱最多包含20个字符!",
                                             }
                             )
    
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                min_length = 6,
                                max_length = 16,
                                label="密码",
                                error_messages={'required': "密码字段不能空!",
                                                'min_length': "密码最少为6个字符!",
                                                'max_length': "密码最多为16个字符!",
                                                },
                                )
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                min_length = 6,
                                max_length = 16,
                                label="确认密码",
                                error_messages={'required': "密码字段不能空!",
                                                'min_length': "密码最少为6个字符!",
                                                'max_length': "密码最多为16个字符!",
                                                },
                                )

    captcha = CaptchaField(label="简单算式",
                           help_text="为了证明你不是机器人，请计算这个简单的数学算式！")
    
    def clean_username(self):
        """
        验证用户名是否有效且不重复。
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("用户名已被占用!")

    def clean_email(self):
        """
        验证邮件地址的唯一性
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("邮件地址已被使用，请另外选择一个!")
        return self.cleaned_data['email']

    def clean_password1(self):
        """
        对密码的复杂度进行验证
        """
        special_letters = '!@#$%^&*()_+-=[]{}\|;:,./<>?'
        has_digit = False
        has_letter = False
        has_special = False

        for c in self.cleaned_data['password1']: 
            if c in string.digits:
                has_digit = True
            elif c in string.ascii_letters:
                has_letter = True
            elif c in special_letters:
                has_special = True

        if has_digit and has_letter and has_special:
            return self.cleaned_data['password1']

        raise forms.ValidationError("密码必须至少包含一个数字,一个字母，一个特殊字符（%s） （不包括外层中文括号）" % special_letters)

    def clean(self):
        """
        对再次密码是否相同的难证
        需要对两个字段进行验证
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("再次输入密码不一致！")

        return self.cleaned_data

class PassChangeForm(forms.Form):
    """更改密码表单
    """
    old_password = forms.CharField(label = "旧密码",
                                   widget=forms.PasswordInput)

    new_password1 = forms.CharField(label="新密码",
                                    widget=forms.PasswordInput,
                                    min_length = 6,
                                    max_length = 16,
                                    error_messages={'required': "密码字段不能空!",
                                                    'min_length': "密码最少为6个字符!",
                                                    'max_length': "密码最多为16个字符!",
                                                    },
                                    )

    new_password2 = forms.CharField(label="确认新密码",
                                    widget=forms.PasswordInput,
                                    min_length = 6,
                                    max_length = 16,
                                    error_messages={'required': "密码字段不能空!",
                                                    'min_length': "密码最少为6个字符!",
                                                    'max_length': "密码最多为16个字符!",
                                                    },
                                    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PassChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        确证旧密码正确
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError("旧密码不对，重新输入")
        return old_password

    def clean_new_password1(self):
        """
        对密码的复杂度进行验证
        """
        special_letters = '!@#$%^&*()_+-=[]{}\|;:,./<>?'
        has_digit = False
        has_letter = False
        has_special = False

        for c in self.cleaned_data['new_password1']: 
            if c in string.digits:
                has_digit = True
            elif c in string.ascii_letters:
                has_letter = True
            elif c in special_letters:
                has_special = True

        if has_digit and has_letter and has_special:
            return self.cleaned_data['new_password1']

        raise forms.ValidationError("密码必须至少包含一个数字,一个字母，一个特殊字符（%s） （不包括外层中文括号）" % special_letters)


    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

