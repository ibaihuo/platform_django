#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.core.management.base import BaseCommand
import sys

class Command(BaseCommand):
    """清除过期的验证码
    """
    help = "清除过期的验证码"
    
    def handle(self, **options):
        from captcha.models import CaptchaStore
        import datetime
        expired_keys = CaptchaStore.objects.filter(expiration__lte=datetime.datetime.now()).count()

        print "Currently %s expired hashkeys" % expired_keys
        try:
            CaptchaStore.remove_expired()
        except:
            print "Unable to delete expired hashkeys."
            sys.exit(1)


        if expired_keys > 0:
            print "Expired hashkeys removed."
        else:
            print "No keys to remove."
