#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('oyea9le', 'oyea9le@gmail.com'),
)


# 用户认证资料
AUTH_PROFILE_MODULE = 'team.TeamProfile'


# 用户注册激活允许时间
ACCOUNT_ACTIVATION_DAYS = 3


# 发送邮件相关配置
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'oyea9le@gmail.com'
EMAIL_HOST_PASSWORD = 'oyea9le123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



MANAGERS = ADMINS

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'hacking',                    # 数据库
        'USER': 'root',                       # 用户名
        'PASSWORD': 'toor',                   # 密码
        'HOST': '',                           # 主机
        'PORT': '',                           # 端口
    }
}

# 时区设置
TIME_ZONE = 'Asia/Chongqing'

# 语言
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'zh-cn'

# 站点ID
SITE_ID = 1

# 默认编码
DEFAULT_CHARSET = 'utf-8'


#日期与时间格式
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'


FORCE_SCRIPT_NAME = ""

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
# 国际化语言支持，提供翻译
#USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
#USE_L10N = True

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(SITE_ROOT, 'site_media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


# hash算法的种子
SECRET_KEY = '8kb2d@5h9h!!=!w^%gond=k_2)ueqy1(c*bgtgsqs89dlsd($e'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware', # 事务支持
#    'mydebug.DebugMiddleWare',
)

ROOT_URLCONF = 'hacking.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'team',
    'forum',
    'captcha',
    'registration',
)
