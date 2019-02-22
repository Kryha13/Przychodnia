from django.shortcuts import render
from django.http import request
from django.views import generic, View
from Clinic.models import Doctors

# Create your views here.
from django.views import View


class MainPage(generic.TemplateView):
    template_name = 'main_page.html'

class DoctorsView(generic.ListView):
    template_name = 'doctors_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctors.objects.all()


class LoginPage(generic.TemplateView):
    template_name = 'login.html'


class RegisterPage(generic.TemplateView):
    template_name = 'register.html'


# class SetVisit(View):
#     def get(self, request):

class SetVisit(generic.TemplateView):
    template_name = 'set_visit.html'

