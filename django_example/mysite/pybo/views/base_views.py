# -*- coding: utf-8 -*-
from django.views import generic
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question

import logging
logger = logging.getLogger(__name__)
# logger = logging.getLogger("pybo")


# generic View
class IndexView(generic.ListView):
    def get_queryset(self):
        # _list.html created
        return Question.objects.order_by("-create_date")


class DetailView(generic.DetailView):
    # _detail.html created
    model = Question


def index(request):
    logger.info("INFO LOG TEST")
    logger.error("ERROR LOG TEST")

    page = request.GET.get("page", "1")
    kw = request.GET.get("kw", "")

    question_list = Question.objects.order_by("-create_date")

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, "kw": kw}
    return render(request, 'pybo/question_list.html', context)
    # return HttpResponse("Welcome Pybo")


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # question = Question.objects.get(id=question_id)
    context = {"question": question} # dict
    return render(request, "pybo/question_detail.html", context)