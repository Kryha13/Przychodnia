"""Project URL Configuration

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
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path, include
from Clinic.views import MainPage, DoctorsView, RegisterView, SetVisit, ContactView, \
    ChangePasswordView, YourAccountView, ActivateView, EditProfileView, VisitsHistoryView, TreatmentHistoryView, \
    SingleVisitView, DoctorInfoView, FacilityDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Common.urls')),
    path('facility/<int:pk>', FacilityDetailView.as_view(), name="facility"),
    path('avatar/', include('avatar.urls')),
    path('', MainPage.as_view(), name='main'),
    path('doctors', DoctorsView.as_view(), name='doctors'),
    path('doctor_info/<doctor_id>', DoctorInfoView.as_view(), name='doctor_info'),
    path('set_visit', SetVisit.as_view(), name='set_visit'),
    path('contact', ContactView.as_view(), name='contact'),
    path('your_account', YourAccountView.as_view(), name='your_account'),
    path('edit_profile', EditProfileView.as_view(), name='edit_profile'),
    path('visits_history', VisitsHistoryView.as_view(), name='visits_history'),
    path('visit/<visit_id>', SingleVisitView.as_view(), name='single_visit'),
    path('treatment_history', TreatmentHistoryView.as_view(), name='results_view'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


