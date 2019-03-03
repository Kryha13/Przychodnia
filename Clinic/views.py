from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import request
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.views.generic import RedirectView

from Clinic.models import Doctors, Accounts, User, Messages
from .forms import UserForm


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
            password_conf = form.cleaned_data['password_conf']
            if password == password_conf:
                user.set_password(password)
                user.is_staff = True
                user.save()
            ##  automatically login after account creation
                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('/your_account')
            else:
                messages = ['Passwords do not match']

            return render(request, self.template_name, {'form': form, 'messages': messages})



class LoginView(View):
    template_name = 'login.html'

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/your_account')

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


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


class YourAccountView(generic.TemplateView):
    template_name = 'my_account.html'


class ChangePasswordView(View):
    template_name = 'change_password.html'

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages = ['Your password has been changed']
            user.save()
            return redirect('/your_account', {'messages': messages})

        return render(request, self.template_name, {'form': form})
