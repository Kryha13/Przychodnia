from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic, View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash

from Clinic.models import User
from Clinic.tokens import account_activation_token
from Clinic.forms import UserForm


# Create your views here.


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