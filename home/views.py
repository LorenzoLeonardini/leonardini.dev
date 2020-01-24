from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage

import requests

# Create your views here.

def index(request):
    return render(request, 'home/index.html')


def contact(request):
    try:
        name = request.POST['name'].strip()
        email = request.POST['email'].strip()
        company = request.POST['company'].strip()
        reason = int(request.POST['reason'].strip())
        if reason < 1 or reason > 5:
            raise Exception('reason is not a valid number')
        message = request.POST['message'].strip()

        if reason == 1:
            subject = 'I want to know you better (C.V., full porfolio...)'
        elif reason == 2:
            subject = 'Regarding one of your projects'
        elif reason == 3:
            subject = 'Job proposal'
        elif reason == 4:
            subject = 'Other'
        elif reason == 5:
            subject = 'I\'m bored'

        URL = 'https://www.google.com/recaptcha/api/siteverify'
        PARAMS = {'secret': '6Ldmmq0UAAAAAH33ZUMbqzwBDFzRu_Vb-kShl4oD', 'response': request.POST['g-recaptcha-response']}

        r = requests.post(url = URL, data = PARAMS)
        captcha = r.json()

        if not captcha['success']:
            raise Exception('failed to verify captcha')

        mail = EmailMessage('[CONTACTS] ' + subject, message, name + ('' if len(company) == 0 else (' *at* ' + company)) + ' <contacts@leonardini.dev>', ['lorenzo@leonardini.dev'], headers= {'Reply-To': email})
        mail.send()
    except Exception as e:
        return HttpResponse('{"success": false}')
    return HttpResponse('{"success": true}')
