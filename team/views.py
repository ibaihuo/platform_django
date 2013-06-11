#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.shortcuts import render_to_response,get_object_or_404,redirect
from django.template import RequestContext,loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from datetime import date,datetime

from team.conf import settings
from team.forms import ProfileForm,SubmitForm,SingleChoiceChallengeForm, MutilChoiceChallengeForm
from team.models import ChoiceChallenge, Challenge,TeamProfile,SubmitLog,Notice
from team.paginator import paginator

#################################################################################################
###################################### Notice Viewer ############################################
#################################################################################################
def notice(request):
    notices = Notice.objects.filter(is_shown=True).order_by('-update_date','pub_date')

    return render_to_response('home/notices.html',
                              paginator(request, notices, settings.NOTICE_PER_PAGE),
                              context_instance=RequestContext(request))

@login_required
def notice_detail(request,notice_id):
    notice = get_object_or_404(Notice,id=notice_id)

    # 隐藏不显示的公告
    if not notice.is_shown:
        raise Http404

    return render_to_response('home/notices_detail.html',
                              {'notice':notice,
                               },
                              context_instance=RequestContext(request))


#################################################################################################
###################################### Rank Viewer ##############################################
#################################################################################################
@login_required
def rank(request):
    profiles = TeamProfile.objects.all().filter(activation_key='ALREADY_ACTIVATED').order_by('-rank','last_submit')

    return render_to_response('rank/rank.html',
                              paginator(request, profiles, settings.RANK_PER_PAGE),
                              context_instance=RequestContext(request)
                              )

@login_required
def rank_report(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=rank-report-%s.txt' % datetime.date(datetime.now())

    profiles = TeamProfile.objects.all().filter(activation_key='ALREADY_ACTIVATED').order_by('-rank','last_submit')
    t = loader.get_template('rank/report_template.txt')
    c = Context({
        'profiles': profiles,
        })
    response.write(t.render(c))

    return response


#################################################################################################
###################################### Profile Viewer ###########################################
#################################################################################################
@login_required
def profile(request):

    current_user = request.user

    # 为管理员或者出题人员建立Profile
    try:
        profile = current_user.get_profile()
    except:
        profile = TeamProfile.objects.create_default(current_user)

    logs = SubmitLog.objects.filter(user=current_user).order_by('-time')

    return render_to_response("profile/profile.html", {
        'profile': profile,
        'logs':logs,
        },
       context_instance=RequestContext(request))


@login_required
def profile_edit(request):
    """用户修改资料
    """

    edit_allow = getattr(settings, "EDIT_ALLOWED", False)

    if not edit_allow:
        return redirect('/accounts/profile/edit_not_allowed')

    try:
        # 获取当前用户资料
        # 不能直接使用TeamProfile.objects.filter(user=request.user.id)
        the_pro = request.user.get_profile()
    except TeamProfile.DoesNotExist:
        the_pro = TeamProfile.objects.create_default(request.user)

    form = ProfileForm()
    
    if request.method == 'POST': 
        form = ProfileForm(request.POST, instance=the_pro)
        if form.is_valid():
            form.save()                 # 更新数据
            return redirect('/accounts/profile')
        else:
            return render_to_response('profile/profile_edit.html',
                                      {'form':form
                                       },
                                      context_instance=RequestContext(request),

                                      )
    else:
        form = ProfileForm(instance=the_pro)
        return render_to_response('profile/profile_edit.html',
                              {'form':form
                               },
                              context_instance=RequestContext(request),
                              )

#################################################################################################
###################################### Challenge Viewer #########################################
#################################################################################################
@login_required
def challenge_choice(request):
    challenges = ChoiceChallenge.objects.all()

    # 获得当前团队已完成的题目列表
    profile = request.user.get_profile()
    cur_fin_chall = str(profile.finished_choices)

    data = paginator(request, challenges, settings.CHALL_PER_PAGE)

    data['cur_fin_chall'] = cur_fin_chall

    return render_to_response('challenge/choice.html',
                              data,
                              context_instance=RequestContext(request))

@login_required
def challenge_choice_detail(request, id):

    challenge = get_object_or_404(ChoiceChallenge, id=id)

    if challenge.c_type == u"单选":
        single = True
        form = SingleChoiceChallengeForm(counts=challenge.c_counts)
    else:
        single = False
        form = MutilChoiceChallengeForm(counts=challenge.c_counts)

    message = ''

    if request.method == 'POST':
        if single:
            form = SingleChoiceChallengeForm(request.POST,counts=challenge.c_counts)
        else:
            form = MutilChoiceChallengeForm(request.POST, counts=challenge.c_counts)

        if form.is_valid():
            answer = form.cleaned_data['answer']
            answer = ''.join(answer)    # 处理多项选择的时候的问题
            if SubmitLog.objects.has_not_submited(request.user.id, 'choice', id):
                # 保存日志，不论答案正确与否
                ip = request.META['REMOTE_ADDR'] # 客户端的IP地址
                user_agent = request.META['HTTP_USER_AGENT'] # 客户端相关信息
                SubmitLog.objects.create_a_log(request.user, id, 'choice', challenge.score, ip, user_agent)

                # 更新完成题目列表,只要用户提交
                profile = request.user.get_profile()
                profile.update_finished('choice', id)

                if answer == challenge.answer:
                    message = "right" # 正确

                    # 更新积分
                    profile.update_rank_submit(challenge.score)

                else:
                    message = "wrong"     # 答案错误
            else:
                message = "submited" # 提交过了的答案


    return render_to_response('challenge/choice_detail.html',
                              {'challenge':challenge,
                               'form':form,
                               'message':message,
                               },
                              context_instance=RequestContext(request))


@login_required
def challenge(request):
    challenges = Challenge.objects.filter(is_shown=True)

    # 获得当前团队已完成的题目列表
    profile = request.user.get_profile()
    cur_fin_chall = str(profile.finished_challenges)

    has_choice = ChoiceChallenge.objects.exists()

    data = paginator(request, challenges, settings.CHALL_PER_PAGE)

    data['has_choice'] = has_choice
    data['cur_fin_chall'] = cur_fin_chall

    return render_to_response('challenge/index.html',
                              data,
                              context_instance=RequestContext(request))


@login_required
def challenge_detail(request,challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    # 保护隐藏的题目不被用户查看到
    if not challenge.is_shown:
        raise Http404

    prev_passed = True
    if not challenge.has_passed_prev(request.user):
        prev_passed = False

    return render_to_response('challenge/detail.html',
                              {'challenge':challenge,
                               'prev_passed':prev_passed,
                               },context_instance=RequestContext(request))


@login_required
def submit_answer(request,challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    submit_closed = getattr(settings, "SUBMIT_CLOSED", False)
    if submit_closed:
        return redirect('/challenge/submit-closed')

    # 保护隐藏的题目不被用户提交答案
    if not challenge.is_shown:
        raise Http404

    # 判断是否挑战通过本题的先决题目
    if not challenge.has_passed_prev(request.user):
        raise Http404

    message_level = "submit"            # 首次提交

    form = SubmitForm()

    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            your_answer = form.cleaned_data['answer']
            if challenge.is_right_answer(your_answer):
                if SubmitLog.objects.has_not_submited(request.user.id,'challenge', challenge_id):
                    message_level = "right" # 正确

                    # 更新积分和完成的题目列表
                    profile = request.user.get_profile()
                    profile.update_rank_submit(challenge.score)
                    profile.update_finished('challenge', challenge.id)

                    # 保存日志
                    ip = request.META['REMOTE_ADDR'] # 客户端的IP地址
                    user_agent = request.META['HTTP_USER_AGENT']
                    SubmitLog.objects.create_a_log(request.user, challenge_id, 'challenge', challenge.score, ip, user_agent)
                else:
                    message_level = "submited" # 提交过了的答案
            else:
                message_level = "wrong"     # 答案错误



    return render_to_response('challenge/submit.html',
                              {'message_level':message_level,
                               'form':form,
                               'challenge':challenge},
                              context_instance=RequestContext(request))
