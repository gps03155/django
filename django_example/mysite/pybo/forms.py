# -*- coding: utf-8 -*-
from django import forms
from pybo.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["subject", "content"]
        # forms.as_p 사용 시 커스텀 위해 필요
        # widgets = {
        #     "subject": forms.TextInput(attrs={"class": "form-control"}),
        #     "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
        # }
        labels = {
            'subject': "Title",
            "content": "Content"
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            "content": "Answer Content"
        }
