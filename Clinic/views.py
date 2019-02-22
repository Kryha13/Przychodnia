from django.shortcuts import render
from django.http import request
from django.views import generic

# Create your views here.
from django.views import View


class MainPage(generic.TemplateView):
    template_name = 'main_page.html'
