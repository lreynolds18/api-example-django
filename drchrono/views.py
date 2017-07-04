# Create your views here.
import logging, logging.config
import sys
import datetime, pytz, requests, time
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')

    context = {
    }
    return HttpResponse(template.render(context, request))

def login(request):
    # requests.get('{}?response_type=code&client_id={}&redirect_uri={}'.format(AUTHORIZE_URL, CLIENT_ID, REDIRECT_URI)) 
    pass

def success(request):
    template = loader.get_template('home.html')

    print(request)
    context = {'request' : request}

    return HttpResponse(template.render(context, request))

def drchrono(request):
    template = loader.get_template('drchrono.html')

    social_user = request.user.social_auth.filter(
        provider='drchrono',
    ).first()

    access_token = social_user.extra_data['access_token']
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }
    
    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next']
    
    # data_of_birth is formatted as YEAR-MN-DA
    today = time.strftime("%m-%d")
    birthday_patients = []
    nodateofbirth = []

    for patient in patients:
        if patient[u'date_of_birth'] == None:
            nodateofbirth.append(patient)
        elif patient[u'date_of_birth'][:5] == today:
            birthday_patients.append(patient)

    context = {
        'patients' : patients,
        'birthday_patients' : birthday_patients,
        'nodateofbirth' : nodateofbirth,
    }
    return HttpResponse(template.render(context, request))

