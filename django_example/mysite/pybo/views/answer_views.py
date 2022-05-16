# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


@login_required(login_url='common:login')
def answer_create(request, question_id):
    '''
    Register Answer
    '''
    question = get_object_or_404(Question, pk=question_id)

    if request.method.upper() == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("{}#answer_{}".format(
                resolve_url("pybo:detail", question_id=question.id), answer.id
            ))
    else:
        return HttpResponseNotAllowed("Only Post is possible.")

    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)

    # question.answer_set.create(content=request.POST.get("content"), create_date=timezone.now())
    # answer = Answer(question=question, content=request.POST.get("content"), create_date=timezone.now())
    # answer.save()
    # return redirect("pybo:detail", question_id=question.id)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:
        messages.error(request, 'unAuthorization')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method.upper() == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect("{}#answer_{}".format(
                resolve_url("pybo:detail", question_id=answer.question.id), answer.id
            ))
    else:
        form = AnswerForm(instance=answer)
    context = {"answer": answer, "form": form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:
        messages.error(request, "unAuthorization")
    else:
        answer.delete()
    return redirect("pybo:detail", question_id=answer.question.id)


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author:
        messages.error(request, 'no vote self answer')
    else:
        answer.voter.add(request.user)
    # return redirect('pybo:detail', question_id=answer.question.id)
    return redirect("{}#answer_{}".format(
        resolve_url("pybo:detail", question_id=answer.question.id), answer.id
    ))
