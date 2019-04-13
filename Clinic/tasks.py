from __future__ import absolute_import, unicode_literals
from celery import task
import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from Clinic.models import Visits


@task()
def email_reminder():
    visits = Visits.objects.filter(date=datetime.date.today() + datetime.timedelta(days=1))
    for visit in visits:
        mail_subject = 'Reminder of visit'
        message = render_to_string('reminder_email.html', {
            'user': visit.patient.user,
            'visit': visit,
        })
        to_email = visit.patient.user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
