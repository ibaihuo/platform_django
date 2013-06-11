#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime
import random
import re

from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.utils.hashcompat import sha_constructor
from team.choices import TEAM_PROFILE

class NoticeManager(models.Manager):
    """
    """
    def set_to_show(self,id):
        """设置显示
        """
        try:
            notice = self.get(id=id)
        except self.model.DoesNotExist:
            return False
        
        notice.is_shown = True
        notice.save()

    def set_to_hide(self,id):
        """设置隐藏
        """
        try:
            notice = self.get(id=id)
        except self.model.DoesNotExist:
            return False
        
        notice.is_shown = False
        notice.save()
 
class LogManager(models.Manager):
    '''日志管理类
    '''
    def has_not_submited(self, user_id, challenge_type, challenge_id):
        """If the user has not successful submited the challenge ,Return True
        """
        # 查无记录
        return not self.filter(user=user_id, challenge_type=challenge_type, challenge_id=challenge_id)


    def create_a_log(self, user, challenge_id, challenge_type, score, ip, user_agent):
        """更新日志
        """

        return self.create(user = user,
                           challenge_id = challenge_id,
                           challenge_type = challenge_type,
                           score = score,
                           ip = ip,
                           user_agent = user_agent,
                           )
    


SHA1_RE = re.compile('^[a-f0-9]{40}$')

class TeamManager(models.Manager):
    """
    """
    def create_default(self, user):
        """Just to create a default TeamProfile for root or administrators
        """
        return self.create(user=user,
                           team_name=u"测试账号",
                           leader_name=u"测试人员",
                           leader_sn="2007122048",
                           university="WEB测试大学",
                           college="WEB测试学院",
                           activation_key=self.model.ACTIVATED,
                           )
    def create_inactive_user(self, username, email, password):
        """创建一个未激活的用户，并创建用户团队的默认扩展属性
        """
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        team_profile = self.create_default_profile(new_user)

        return team_profile.activation_key

    # 应用事务
    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def create_default_profile(self, user):
        """
        Create a ``TeamProfile`` for a given ``User``, and return the ``TeamProfile``.
        """
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        username = user.username
        activation_key = sha_constructor(salt+username).hexdigest()

        return self.create(user=user,
                           activation_key = activation_key,
                           team_name = TEAM_PROFILE['team_name'],
                           leader_name = TEAM_PROFILE['leader_name'],
                           leader_phone = TEAM_PROFILE['leader_phone'],
                           leader_sn = TEAM_PROFILE['leader_sn'],
                           mem1_name = TEAM_PROFILE['mem1_name'],
                           mem1_sn = TEAM_PROFILE['mem1_sn'],
                           mem2_name = TEAM_PROFILE['mem2_name'],
                           mem2_sn = TEAM_PROFILE['mem2_sn'],
                           mem3_name = TEAM_PROFILE['mem3_name'],
                           mem3_sn = TEAM_PROFILE['mem3_sn'],
                           university = TEAM_PROFILE['university'],
                           college = TEAM_PROFILE['college'],
                           )


    def real_activate_user(self, activation_key):
        """
        由管理员真正激活用户
        """
        # 不符合sha1匹配规则的时候，不需要带到数据库查询
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                return user
        return False

    def fake_activate_user(self, activation_key):
        """
        引导用户进行激活，填写资料，并不真正激活用户
        """
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                return profile

        return False


    def deactivate_user(self,profile):
        user = profile.user
        user.is_active = False
        user.save()

    def delete_expired_users(self):
        """
        """
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()
