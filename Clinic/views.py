from datetime import date

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.views.generic import RedirectView
from django.contrib.auth.models import User
from Clinic.models import Doctors, Accounts, User, Messages, Visits, Patient, Results
from Clinic.tokens import account_activation_token
from .forms import UserForm, EditProfileForm, VisitsHistoryForm, TreatmentHistoryForm, SetVisitForm


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
                user.is_active = False
                user.save()
                # user = authenticate(username=username, password=password)
                current_site = get_current_site(request)
                mail_subject = 'Activate your clinic account.'
                message = render_to_string('activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, 'Please confirm your email address by '
                                          'activation link to complete the registration')
                return redirect('/')
                # if user is not None:
                #     if user.is_active:
                #         login(request, user)
                #         return redirect('/your_account')
            else:
                messages.error(request, 'Passwords did not match')

        return render(request, self.template_name, {'form': form})


class ActivateView(View):
    template_name = 'main_page.html'

    def get(self,request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'chujdupa')
            return redirect('/')
        if user is not None:
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                login(request, user)
                messages.success(request, 'Email confirmed. You are logged in now.')
                return redirect('/')
        else:
            messages.error(request, 'Activation link is invalid')
            return redirect('/')
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'login.html'

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/your_account')
        else:
            messages.error(request, 'Wrong username or password')
            return redirect('/login')

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SetVisit(View):
    template_name = 'set_visit.html'
    form_class = SetVisitForm

    def get(self, request):
        form = self.form_class(
            initial={
                'patient': request.user,
                'date': date.today(),
            })
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = form.cleaned_data.get('patient')
            visit.doctor = form.cleaned_data.get('doctor')
            visit.date = form.cleaned_data.get('date')
            visit.hour = form.cleaned_data.get('hour')
            if Visits.objects.filter(hour=visit.hour, doctor=visit.doctor,
                                     date=visit.date).exists():
                messages.error(request, 'This term is already booked')
                return redirect('/set_visit')
            else:
                visit.save()
                messages.success(request, 'Your visit has been set')
                return redirect('/your_account')
        return render(request, self.template_name, {'form': form})


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        text = request.POST.get('text')
        patient = User.objects.get(id=request.POST.get('user'))

        Messages.objects.create(first_name=first_name, last_name=last_name,
                                email=email, text=text, patient=patient)

        return redirect('/')


class YourAccountView(generic.TemplateView):
    template_name = 'my_account.html'


class EditProfileView(View):
    template_name = 'edit_profile.html'
    form_class = EditProfileForm

    def get(self, request):
        user = request.user
        form = self.form_class(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
        })
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            user.first_name =form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Your changes have been saved')
            return redirect('/your_account')
        return render(request, self.template_name, {'form': form})


class VisitsHistoryView(generic.ListView):
    template_name = 'visits_history.html'
    context_object_name = 'visits'

    def get_queryset(self):
        return Visits.objects.filter(patient=self.request.user.id)


class SingleVisitView(View):
    template_name = 'single_visit.html'

    def get(self, request, visit_id):
        patient = request.user.id
        if Results.objects.filter(patient=patient, visit=Visits.objects.get(pk=visit_id)).exists():
            results = Results.objects.filter(patient=patient, visit=Visits.objects.get(pk=visit_id))
            return render(request, self.template_name, {'results': results})
        else:
            messages.error(request, 'There are no results available for this visit yet.')
            return render(request, self.template_name)


class TreatmentHistoryView(View):
    template_name = 'treatment_history.html'

    def get(self, request):
        patient = request.user.id
        results = Results.objects.filter(patient=patient)
        return render(request, self.template_name, {'results': results})


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
            # messages = ['Your password has been changed']
            user.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/your_account')

        return render(request, self.template_name, {'form': form})

