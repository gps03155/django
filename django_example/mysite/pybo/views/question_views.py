# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
    if request.method.upper() == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {"form": form}

    return render(request, "pybo/question_form.html", context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, 'unAuthorization')
        return redirect('pybo:detail', question_id=question.id)

    if request.method.upper() == "POST":
        # request.POST 값으로 question 덮어쓰기
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        # question 값으로 form 값 채우기 (instance 속성)
        form = QuestionForm(instance=question)

    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "unAuthorization")
        return redirect("pybo:detail", question_id=question.id)

    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
        messages.error(request, "not vote self question")
    else:
        question.voter.add(request.user)
    return redirect("pybo:detail", question_id=question.id)

