#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib.auth.models import Group as DjangoGroup

gUsers = DjangoGroup(name='Users')

  
gUsers.save()
gGroupAdmins = DjangoGroup(name='GroupAdmins')
gGroupAdmins.save()

# Set users
zen = User.objects.create_user('zen', 'zen@emailaddress',
                               'pwd123')
zen.groups = [gUsers] 
