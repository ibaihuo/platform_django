#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.contrib import admin
from team.models import ChoiceChallenge,Challenge,Notice,Person,Trophy,TeamProfile, SubmitLog,Pic,Tarball

class TeamProfileAdmin(admin.ModelAdmin):
    ordering = ('-rank','last_submit')
    actions = ['activate_users','deactivate_users']
    list_per_page = 10
    list_display=('user','team_name','rank','finished_challenges',
                  'leader_name','leader_phone','leader_sn',
                  'mem1_name','mem1_sn','mem2_name','mem2_sn','mem3_name','mem3_sn',
                  'university', 'college',
                  'activation_key','activation_key_expired')
    # 能搜索的字段
    search_fields = ('user__username','team_name','rank','leader_name','university', 'college')

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady activated.
        """
        for profile in queryset:
            TeamProfile.objects.real_activate_user(profile.activation_key)

    activate_users.short_description = u"激活用户"

    def deactivate_users(self, request, queryset):
        """
        deactivates the selected users, if they are alrady activated.
        """
        for profile in queryset:
            TeamProfile.objects.deactivate_user(profile)

    deactivate_users.short_description = u"禁止用户"

class NoticeAdmin(admin.ModelAdmin):
    ordering = ('-update_date','-pub_date')
    actions = ['set_to_show', 'set_to_hide']
    list_per_page = 10
    list_display = ('id','is_shown','title','author','content','update_date', 'pub_date')
    list_display_links = ('title','id',)
    list_filter = ('author','is_shown',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super(NoticeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def set_to_show(self, request, queryset):
        """显示所有选择的列表
        """
        for notice in queryset:
            Notice.objects.set_to_show(notice.id)

    set_to_show.short_description = u"显示选择项"

    def set_to_hide(self, request, queryset):
        """隐藏所有选择的列表
        """
        for notice in queryset:
            Notice.objects.set_to_hide(notice.id)

    set_to_hide.short_description = u"隐藏选择项"


class PersonAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display=('name','rp', 'grade','advantages','brief','pic')
    list_filter = ('rp','grade',)

class ChoiceChallengeAdmin(admin.ModelAdmin):
    ordering = ('-datetime',)
#    radio_fields = {"answer": admin.VERTICAL}
    list_per_page = 10
    list_display=('id','answer', 'score','c_type','title', 'content','datetime')
    list_display_links=('id','title',)

class ChallengeAdmin(admin.ModelAdmin):
    ordering = ('-datetime',)
    fieldsets = (
        ('关联人物',{
            'fields':('person',)
            }),
        ('关联奖品',{
            'fields':('trophy',)
            }),

        ('题目信息', {
            'fields':('is_shown','prev','author','score','answer','description','url','url_bak')
            }),
        )
#    raw_id_fields = ("author",)
    list_per_page = 10
    list_filter = ('is_shown','author',)
    list_display=('id','prev','person','trophy','score','is_shown','answer','author','url','url_bak','description','datetime',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super(ChallengeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class SubmitLogAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('user', 'challenge_id','challenge_type','ip','user_agent', 'time',)

class TrophyAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display=('name', 'grade','classify','brief','pic')


admin.site.register(Pic)
admin.site.register(Tarball)
admin.site.register(ChoiceChallenge,ChoiceChallengeAdmin)
admin.site.register(TeamProfile, TeamProfileAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(SubmitLog, SubmitLogAdmin)
admin.site.register(Trophy, TrophyAdmin)
