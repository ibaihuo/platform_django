#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db.models.signals import post_save
from forum.models import Forum
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.hashcompat import sha_constructor
import datetime

from team.managers import LogManager,TeamManager,NoticeManager
from choices import *

class Notice(models.Model):
    """新闻公告
    """
    is_shown = models.BooleanField("显示",default=True)
    classify = models.CharField("类别",max_length=40, choices=NOTICES_CLASSIFY,default=u'挑战公告')
    title = models.CharField("标题",max_length=200)
    author = models.ForeignKey(User, verbose_name="发布作者")
    content = models.TextField("内容")
    pub_date = models.DateTimeField("发布日期",auto_now_add=True) # 发布时间
    update_date = models.DateTimeField("更新日期",auto_now=True) # 更新时间

    objects = NoticeManager()

    class Meta:
        ordering = ('-update_date',)

    def __unicode__(self):
        return self.title

    def get_prev(self):
        """
        Retrun prev Notice
        """
        notice_prev = Notice.objects.filter(is_shown__exact=True).order_by('-id').filter(id__lt=self.id)

        if notice_prev.count() > 0:
            return notice_prev[0].id
        else:
            return None

    def get_next(self):
        """
        Retrun next Notice
        """
        notice_next = Notice.objects.filter(is_shown__exact=True).order_by('id').filter(id__gt=self.id)

        if notice_next.count() > 0:
            return notice_next[0].id
        else:
            return None

class Pic(models.Model):
    """Image for flatpages
    """
    pic = models.ImageField("图片", upload_to='flatpage/pic')

    class Meta:
        db_table = "flat_pic"

class Tarball(models.Model):
    """Tarball for flatpages
    """
    tarball = models.FileField("答题包", upload_to='flatpage/tarball')

    class Meta:
        db_table = "flat_tarball"


class Person(models.Model):
    """挑战人物
    """
    name = models.CharField("名字",max_length=40,unique=True)
    rp = models.CharField("人品",choices=RP, max_length=30)   # 人品
    grade = models.CharField("人物等级",max_length=40, choices=PERSON_GRADE)
    advantages = models.CharField("强项",max_length=80)
    brief = models.TextField("简介",max_length=200)
    pic = models.ImageField("图片",upload_to='images/person')

    def __unicode__(self):
        return self.name


class Trophy(models.Model):
    """挑战奖品
    """
    name = models.CharField('名称',max_length=40,unique=True)
    grade = models.CharField('级别',max_length=40,choices=TROPHY_GRADE)
    classify = models.CharField('类别', max_length=40, choices=TROPHY_CLASSIFY)
    brief = models.TextField('介绍',max_length=200)
    pic = models.ImageField('图片',upload_to='images/trophy')

    def __unicode__(self):
        return self.name


class ChoiceChallenge(models.Model):
    """This is for Choice challenge.
    """
    score = models.IntegerField("分值", default=1, choices=SCORE_CHOICE)
    c_type = models.CharField("选择类型",default=u'单选',choices=CHOICE_TYPE,max_length=10)
    c_counts = models.IntegerField("选项总个数",default=4, choices=CHOICE_COUNT, max_length=1, help_text=u"请正确选择选项的总个数")
    answer = models.CharField("答案", max_length=20, help_text=u"大写字母，且按顺序输入ABCD")
    title = models.TextField("题目")
    content = models.TextField("内容")
    datetime = models.DateTimeField('创建时间',auto_now_add=True)

    def get_prev(self):
        """
        Retrun prev choice
        """
        choice_prev = Choice.objects.filter(is_shown__exact=True).order_by('-id').filter(id__lt=self.id)

        if choice_prev.count() > 0:
            return choice_prev[0].id
        else:
            return None

    def get_next(self):
        """
        Retrun next Choice
        """
        choice_next = Choice.objects.filter(is_shown__exact=True).order_by('id').filter(id__gt=self.id)

        if choice_next.count() > 0:
            return choice_next[0].id
        else:
            return None


class Challenge(models.Model):
    """挑战题目
    """
    is_shown = models.BooleanField("显示",default=False,max_length=1)
    author = models.ForeignKey(User, verbose_name="出题人")
    score = models.IntegerField("分值",default=1, choices=SCORE_CHOICE)
    answer = models.CharField("答案", max_length=40)#,validators=[MinLengthValidator(8)])
    description = models.TextField("描述",max_length=80)
    prev = models.ForeignKey('self', verbose_name="挑战前提", null=True, blank=True)    # ForeighKey self
    person = models.OneToOneField(Person, verbose_name="人物")                     # 1对1的关系
    trophy = models.ForeignKey(Trophy, verbose_name="奖品")
    url = models.URLField(verify_exists=False)
    url_bak = models.URLField(verify_exists=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        # 加密答案字段
        self.answer = sha_constructor(self.answer).hexdigest()[4:-4]

        super(Challenge,self).save(*args,**kwargs)

    def __unicode__(self):
        return  "%s-%s-%s" %(str(self.id), self.person.name, self.trophy)

    def is_right_answer(self, answer):
        """To judge the answer is right or not
        """
        return self.answer == sha_constructor(answer).hexdigest()[4:-4]

    def has_passed_prev(self, user):
        """To judge if the current challenge 's prev challenge is passed or not.
        passed: True
        Not Passed: False
        """
        if self.prev:
            finished = user.get_profile().get_finished()
            #print finished,self.prev.id
            if str(self.prev.id) not in finished:
                return False

        return True

    def get_absolute_url(self):
        """
        """
        return '%s%i/' % (reverse('challenge_index'), self.id)

    # def get_absolute_url(self):
    #     return ('challenge_detail', [self.id])

    #get_absolute_url = models.permalink(get_absolute_url)


class TeamProfile(models.Model):
    """团队扩展属性
    """
    user = models.ForeignKey(User, unique=True,verbose_name="所属团队")
    team_name = models.CharField('团队名', max_length=50)


    # 队长信息
    leader_name = models.CharField('队长姓名', max_length = 50)
    leader_phone = models.CharField('队长手机', max_length = 11)
    leader_sn = models.CharField('队长学号', max_length = 10)

    # 成员信息
    mem1_name = models.CharField("成员1", max_length = 50, blank=True)
    mem1_sn = models.CharField('成员1－学号', max_length = 10, blank = True)
    mem2_name = models.CharField("成员2", max_length = 50, blank=True)
    mem2_sn = models.CharField('成员2－学号', max_length = 10, blank = True)
    mem3_name = models.CharField("成员3", max_length = 50, blank=True)
    mem3_sn = models.CharField('成员3－学号', max_length = 10, blank = True)

    # 大学及专业
    university = models.CharField('学校', max_length = 50, choices=UNIVERSITY_CHOICE, blank = True)
    college = models.CharField('学院', max_length = 50, choices=COLLEGE_CHOICE,blank = True)

    # 分数不可更改
    rank = models.IntegerField('分数', default=0, blank=True, editable=False)

    # 答题情况
    finished_challenges = models.CommaSeparatedIntegerField("完成挑战题目",max_length=300,blank=True,editable=False)
    finished_choices = models.CommaSeparatedIntegerField("完成选择题目",max_length=300,blank=True,editable=False)
    last_submit = models.DateTimeField("最后提交", blank=True, null=True, editable=False)

    # 激活码
    activation_key = models.CharField('激活码', max_length=40)

    ACTIVATED = u"ALREADY_ACTIVATED"

    objects = TeamManager()

    class Meta:
        ordering = ('-rank','-last_submit')


    def __unicode__(self):
        return u"Team information for team %s" % self.user


    def get_current_rank(self):
        usernames = TeamProfile.objects.values_list('user__username', flat=True).order_by('-rank', 'last_submit')

        return list(usernames).index(self.user.username) + 1

    def get_finished(self):
        if not self.finished_challenges:
            return []

        return self.finished_challenges.split(',')

    def update_finished(self, challenge_type, challenge_id):
        """更新用户完成的题目
        """
        challenge_id = str(challenge_id)
        if challenge_type == "challenge":
            if not self.finished_challenges: # 用户第一次提交
                fin = challenge_id
            else:
                fin = self.finished_challenges + "," + challenge_id

            # 更新用户完成的挑战题列表
            self.finished_challenges = fin
            self.save()

        elif challenge_type == "choice":
            if not self.finished_choices:
                fin = challenge_id
            else:
                fin = self.finished_choices + "," + challenge_id

            # 更新用户完成的选择题列表
            self.finished_choices = fin
            self.save()

    def update_rank_submit(self, score):
        """更新用户的积分，和最后提交的时间
        1、加分
        2、更新最后提交时间
        """
        self.rank += score
        self.last_submit = datetime.datetime.now()

        self.save()

    def finished_count(self):
        """统计当前团队完成挑战题目数
        len_x: 完成的挑战题目数
        len_y: 完成的选择题目数
        """
        if not self.finished_challenges:
            len_x = 0
        else:
            len_x = len(self.finished_challenges.split(','))            

        if not self.finished_choices:
            len_y = 0
        else:
            len_y = len(self.finished_choices.split(','))

        return len_x + len_y

    def latest_submit(self):
        """获取用户最后一次提交的时间
        """
        try:
            last = SubmitLog.objects.filter(user=self.user).latest('time').time
        except SubmitLog.DoesNotExist:
            last = "Haven't Submit Yet"

        return last

    def activation_key_expired(self):
        """
        判断用户的激活码是否过期，
        已经激活的用户返回True，
        通过用户的注册时间和设定的过期时间来判断。
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True

class SubmitLog(models.Model):
    """团队提交答案日志
    """
    user = models.ForeignKey(User,editable=False)
    challenge_id = models.CharField(max_length=20,editable=False)
    challenge_type = models.CharField(max_length=20,choices=(('challenge','challenge'),('choice','choice')),editable=False)
    score = models.IntegerField(editable=False)
    time = models.DateTimeField(auto_now_add=True,)
    ip = models.IPAddressField(editable=False)
    user_agent = models.CharField(max_length=200,editable=False)

    objects = LogManager()

    # 表的元信息
    class Meta:
        ordering = ('challenge_type','challenge_id')
        unique_together = (('challenge_id','user','challenge_type'),) # 这两个的组合应该是唯一的

    def __unicode__(self):
        return "SubmitLog for team %s" % self.user
