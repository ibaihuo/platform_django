#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from team.models import TeamProfile
from django.forms import ModelForm
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError

from choices import ANSWER_CHOICE


class SingleChoiceChallengeForm(forms.Form):
    """单项选择题的表单
    动态根据选项个数来创建
    """
    def __init__(self, *args, **kwargs):
        counts = kwargs.pop('counts')
        super(SingleChoiceChallengeForm, self).__init__(*args, **kwargs)

        self.fields['answer'] = forms.ChoiceField(label="请选择一个答案",
                                       widget=forms.RadioSelect(),
                                       choices=ANSWER_CHOICE[:counts],
                                       )

class MutilChoiceChallengeForm(forms.Form):
    """多项或不定项选择题的表单
    动态根据选项个数来创建
    """
    def __init__(self, *args, **kwargs):
        counts = kwargs.pop('counts')
        super(MutilChoiceChallengeForm, self).__init__(*args, **kwargs)

        self.fields['answer'] = forms.MultipleChoiceField(label="请选择一个或多个答案",
                                       widget=forms.CheckboxSelectMultiple(),
                                       choices=ANSWER_CHOICE[:counts],
                                       )
    
class ProfileForm(ModelForm):
    """团队资料表单
    """
    class Meta:
        model = TeamProfile
        exclude = ('user', 'rank','finished_challenges','finished_choices' ,'activation_key')     # 不让用户更改这些字段

    # 数据格式验证
    team_name = forms.CharField(label="团队名称",
                                min_length = 3,
                                max_length=8,
                                error_messages={'required': "方便记忆，必须输入团队名字！",
                                                'min_length': "团队名最少包含3个字符!",
                                                'max_length': "答案最多包含8个字符!",
                                                }
                                )

    leader_name = forms.CharField(label="队长姓名",
                                min_length = 2,
                                max_length = 4,
                                error_messages={'required': "必须输入团队队长的姓名！",
                                                'min_length': "团队名最少包含2个汉字!",
                                                'max_length': "答案最多包含4个汉字!",
                                                }
                                )
                                
    leader_phone = forms.RegexField(regex=r'1\d{10}',
                                    label="队长手机号",
                                    max_length = 11,                                    
                                    error_messages={'required': "请输入真实且有效的手机号!",
                                                    'invalid': "手机号码，必须以1开头，共11位数字！"
                                                    }
                                    )

    leader_sn = forms.RegexField(regex=r'20\d{8}',
                                    label="队长学号",
                                    max_length = 10,                                    
                                    error_messages={'required': "请输入真实且有效的学号!",
                                                    'invalid': "学号必须以20开头，共10位数字"
                                                    }
                                    )


class SubmitForm(forms.Form):
    """提交挑战题目的表单
    """
    answer = forms.RegexField(regex=r'^[\w!@#\%\$\^&\*\(\)\-\+=\?]+$',
                              label="答案",
                              min_length = 6,
                              max_length=64,
                              error_messages={'required': "请填入答案!",
                                              'min_length': "答案最少包含6个字符!",
                                              'max_length': "答案最多包含64个字符!",
                                              'invalid': "答案不合法！只能包含  ［abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!@#$%^&*()-=+?］  (不含外层中文方括号)",}
                              )
    captcha = CaptchaField(label="简单算式",
                           help_text="为了证明你不是机器人，请计算这个简单的数学算式！")
