from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


# generic View
class IndexView(generic.ListView):
    def get_queryset(self):
        # _list.html created
        return Question.objects.order_by("-create_date")


class DetailView(generic.DetailView):
    # _detail.html created
    model = Question


def index(request):
    page = request.GET.get("page", "1")
    question_list = Question.objects.order_by("-create_date")

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)
    # return HttpResponse("Welcome Pybo")


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # question = Question.objects.get(id=question_id)
    context = {"question": question} # dict
    return render(request, "pybo/question_detail.html", context)


def answer_create(request, question_id):
    '''
    Register Answer
    '''
    question = get_object_or_404(Question, pk=question_id)

    if request.method.upper() == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        return HttpResponseNotAllowed("Only Post is possible.")

    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)

    # question.answer_set.create(content=request.POST.get("content"), create_date=timezone.now())
    # answer = Answer(question=question, content=request.POST.get("content"), create_date=timezone.now())
    # answer.save()
    # return redirect("pybo:detail", question_id=question.id)


def question_create(request):
    if request.method.upper() == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {"form": form}

    return render(request, "pybo/question_form.html", context)
