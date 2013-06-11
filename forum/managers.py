#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from django.db.models import Q

class ForumManager(models.Manager):
    """论坛表级别的管理
    """
    def for_groups(self, groups):
        """groups: 为当前用户所属所有组名
        """
        if groups:
            public = Q(groups__isnull=True) # 查询条件：相当于where groups is null
            user_groups = Q(groups__in=groups) # 查询条件：相当于where 论坛所属组，也在用户属性组中

            return self.filter(public|user_groups).distinct() # 去掉重复的行

        return self.filter(groups__isnull=True)
    
    def has_access(self, current_forum, groups):
        """判断当前用户是否有本论坛版块的权限
        current_forum: 当前论坛版块的权限
        current_user: 当前用户的权限
        """
        
        return current_forum in self.for_groups(groups)
