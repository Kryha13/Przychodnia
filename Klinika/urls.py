"""Klinika URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Clinic.views import MainPage, DoctorsView, RegisterView, SetVisit, LoginView, ContactView, LogoutView, \
    ChangePasswordView, YourAccountView, ActivateView, EditProfileView, VisitsHistoryView, TreatmentHistoryView, \
    SingleVisitView
from Klinika import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('doctors', DoctorsView.as_view()),
    path('login/', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('set_visit', SetVisit.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact', ContactView.as_view()),
    path('your_account', YourAccountView.as_view()),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('edit_profile', EditProfileView.as_view(), name='edit_profile'),
    path('visits_history', VisitsHistoryView.as_view(), name='visits_history'),
    path('visit/<visit_id>', SingleVisitView.as_view(), name='single_visit'),
    path('treatment_history', TreatmentHistoryView.as_view(), name='results_view'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


