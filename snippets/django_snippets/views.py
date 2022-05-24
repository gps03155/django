from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django_snippets.models import Snippet
from django_snippets.serializers import SnippetSerializer


# Create your views here.
