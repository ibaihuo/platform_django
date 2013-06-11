#!/usr/bin/env python
#-*- coding:utf-8 -*-

def str_2_tuple(str,integer=False):
    '''将以空格分隔的字符串变成一个元组
    str = u"挑战公告 注意事项 发奖事项 其它"
    integer 表示是否是整数
    tuple = (
    (u"挑战公告", u"挑战公告"),
     u"注意事项",u"发奖事项"),
     ...
    )
    '''
    li = []
    for t in str.split(' '):
        if integer:
            t = int(t)
        li.append((t,t))

    return tuple(li)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

notices = u"挑战公告 注意事项 发奖事项 其它"
NOTICES_CLASSIFY = str_2_tuple(notices)
#print NOTICES_CLASSIFY
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

choice_answer = "A B C D E F G H I J"
ANSWER_CHOICE = str_2_tuple(choice_answer)
#print ANSWER_CHOICE
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

types = u"单选 多选 不定项"
CHOICE_TYPE = str_2_tuple(types)
#print CHOICE_TYPE
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

c_counts = "4 5 6 7 8 9"
CHOICE_COUNT = str_2_tuple(c_counts, integer=True)
#print CHOICE_COUNT

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
rps = u"正派 亦正亦斜 恶人"
RP = str_2_tuple(rps)
#print RP
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

grades = u"散魔 地魔 法魔 真魔 元魔 天魔 魔王 魔君 魔神 毁魔"
PERSON_GRADE = str_2_tuple(grades)
#print PERSON_GRADE

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
scores = "1 2 3 4 5 6 7 8"
SCORE_CHOICE = str_2_tuple(scores,integer=True)
#print SCORE_CHOICE

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

trophy_grades = u"小行江湖 与人对抗 小胜恶人 谁与争峰"
TROPHY_GRADE = str_2_tuple(trophy_grades)
#print TROPHY_GRADE
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
trophy_classifies = u"刀 剑 棍 绝学 丹药"

TROPHY_CLASSIFY = str_2_tuple(trophy_classifies)
#print TROPHY_CLASSIFY
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
universities = u"成都信息工程学院 外界Hacker"


colleges = u"网络工程学院 计算机学院 软件工程学院 大气科学学院 资源环境学院 电子工程学院（大气探测学院） 通信工程学院 控制工程学院 管理学院 数学学院 光电技术学院 外国语学院 政治学院 文化艺术学院 统计学院 商学院 软件与服务外包学院 继续教育学院 银杏学院 网络商学院 其它学院"


UNIVERSITY_CHOICE = str_2_tuple(universities)

COLLEGE_CHOICE = str_2_tuple(colleges)
#print UNIVERSITY_CHOICE
#print COLLEGE_CHOICE
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#下面是配置团队的默认信息
TEAM_PROFILE = {
    "team_name":u"攻防团队",
    "leader_name":u"Joy",
    "leader_phone":"18612345678",
    "leader_sn":"2012123100",
    "mem1_name":u"张三",
    "mem1_sn":"2012123101",
    "mem2_name":u"李四",
    "mem2_sn":"2012123102",
    "mem3_name":u"王五",
    "mem3_sn":"2012123103",
    "university":u"成都信息工程学院",
    "college":u"网络工程学院",
    }

#print TEAM_PROFILE['leader_sn']
