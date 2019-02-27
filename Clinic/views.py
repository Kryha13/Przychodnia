from django.shortcuts import render, redirect
from django.http import request
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from Clinic.models import Doctors, Accounts, User, Messages
from .forms import UserForm
from django.contrib.auth.views import LogoutView


# Create your views here.

class MainPage(generic.TemplateView):
    template_name = 'main_page.html'


class DoctorsView(generic.ListView):
    template_name = 'doctors_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctors.objects.all()


class RegisterView(View):
    form_class = UserForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.is_staff = True
            user.save()

            # return redirect('/')

            ##  automatically login after account creation

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')

        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'login.html'

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        # return render(request, 'main_page.html')

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/')


class SetVisit(generic.TemplateView):
    template_name = 'set_visit.html'


class ContactView(View):
    template_name ='contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        text = request.POST.get('text')
        patient = User.objects.get(id=request.POST.get('user'))

        Messages.objects.create(first_name=first_name, last_name=last_name, email=email, text=text, patient=patient)

        return redirect('/')
