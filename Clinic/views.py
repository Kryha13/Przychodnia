from datetime import date

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic, View
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.views.generic import UpdateView

from Clinic.models import Doctors, Accounts, User, Messages, Visits, Patient, Results, Facility
from Clinic.tokens import account_activation_token
from .forms import UserForm, EditProfileForm, SetVisitForm, YourAccountForm, ContactForm, FacilityDetailForm


# Create your views here.


class MainPage(generic.TemplateView):
    template_name = 'main_page.html'


class DoctorsView(generic.ListView):
    template_name = 'doctors_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctors.objects.all().order_by('category__name')


class DoctorInfoView(View):
    template_name = 'doctor_info.html'

    def get(self, request, doctor_id):
        doctor = Doctors.objects.get(id=doctor_id)
        return render(request, self.template_name, {'doctor': doctor})


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
            password = form.cleaned_data['password']
            password_conf = form.cleaned_data['password_conf']
            if password == password_conf:
                user.set_password(password)
                user.is_staff = True
                user.is_active = False
                user.save()
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
            else:
                messages.error(request, 'Passwords did not match')
        return render(request, self.template_name, {'form': form})


class ActivateView(View):
    template_name = 'base.html'

    def get(self,request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'User does not exists')
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


class SetVisit(View):
    template_name = 'set_visit.html'
    form_class = SetVisitForm

    def get(self, request):
        form = self.form_class(
            initial={
                'patient': request.user.first_name + " " + request.user.last_name,
                'date': date.today(),
            })
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
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
    form_class = ContactForm

    def get(self, request):
        patient = request.user
        if patient.is_authenticated:
            form = self.form_class(initial={
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'email': patient.email,
                'patient': patient,
            })
        else:
            form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent')
            return redirect('/')
        return render(request, self.template_name, {'form': form})


class YourAccountView(View):
    template_name = 'my_account.html'
    form_class = YourAccountForm

    def get(self, request):
        form = self.form_class
        patient = Patient.objects.get(user=request.user)
        return render(request, self.template_name, {'form': form, 'patient': patient})

    def post(self, request):
        patient = Patient.objects.get(user=request.user)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            patient.image = form.cleaned_data['image']
            patient.save()
            messages.success(request, 'Your profile image has been saved')
            return redirect('/your_account')
        return render(request, self.template_name, {'form': form, 'patient': patient})


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
            user.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/your_account')
        return render(request, self.template_name, {'form': form})


class FacilityDetailView(UpdateView):
    form_class = FacilityDetailForm
    model = Facility
    template_name = "facility_detail.html"

