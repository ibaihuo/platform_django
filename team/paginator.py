#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.core.paginator import Paginator
from django.conf import settings

def paginator(request, objects, per_page):
    page_number = 1
    try:
        page_number = int(request.GET.get("page", "1"))
    except:
        pass 
   
    paginator = Paginator(objects, per_page)

    if page_number > paginator.num_pages or page_number < 1:
        page_number = 1

    page = paginator.page(page_number) 


    num_pages = paginator.num_pages

    # Reduce pages in paginator to 10 items
    index_from = 0
    index_to = num_pages

    if num_pages > 10:
        prev_len = len(paginator.page_range[:page_number]) - 1
        next_len = len(paginator.page_range[page_number:])
       
        if prev_len >= 4 and next_len >= 4:
            index_from = page_number - 5 
            index_to = page_number + 4
        else:
            if page_number <= 5:
                index_from = 0 
                index_to = 9
            else:
                index_from = num_pages - 9
                index_to = num_pages 
    
    page_range = paginator.page_range[index_from:index_to] 

    #print num_pages,page

    return {'paginator': paginator, 'page': page, 'page_current': page_number, 
            'page_range': page_range } 
