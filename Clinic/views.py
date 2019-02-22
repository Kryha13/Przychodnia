from django.shortcuts import render
from django.http import request

# Create your views here.


def main_page(request):
    return render(request, 'main_page.html')
