#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.template import Library

register = Library()

rank_name = u"状元 榜眼 探花 进士 会元 贡士 解元 举人 秀才 童生"

ranking = []

for r in rank_name.split(" "):
    ranking.append(r)

def rank_name(rank):
    """
    rank  --> rank_name
    1     --> 状元
    2     --> 榜眼
    """
    if rank < 10:
        return ranking[rank-1]
    else:
        return ranking[9]

register.filter('rank_name', rank_name)
