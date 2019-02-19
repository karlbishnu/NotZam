import os
import logging

from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.utils.datastructures import MultiValueDict

# Create your views here.
from common.model.model import get_model_summary

logger = logging.getLogger('notzam')


def home(request):
    return render(request, 'ml_home.html')


def model_summary(request: HttpRequest):
    return render(request, 'model_summary.html', {'model_summary': get_model_summary()})


