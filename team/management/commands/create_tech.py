#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User,Group

class Command(BaseCommand):
    args = '<name name ...>'
    help = 'Create Default Groups'

    def handle(self, *args, **options):
	for name in args:
            mygroup, created = Group.objects.get_or_create(name=name)
            for p in range(22,58):
                mygroup.permissions.add(p)

            self.stdout.write('Successfully Created Group: "%s"\n' % name)
