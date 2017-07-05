# Create your views here.
import logging, logging.config
import sys
import datetime, pytz, requests, time, threading
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from utils import send_email, send_text

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

    # TODO: fix this - doesn't actually pull current user's access token
    social_user = request.user.social_auth.filter(
        provider='drchrono',
    ).first()

    headers = {
        'Authorization': 'Bearer %s' % social_user.extra_data['access_token'],
    }

    # get current user (doctor) 
    response = requests.get('https://drchrono.com/api/users/current', headers=headers)
    response.raise_for_status()
    data = response.json()
    link = "https://" + data['username'] + ".drchrono.com/patients/"

    # get the current user's last name
    response = requests.get('https://drchrono.com/api/doctors?username=%s' % data['username'], headers=headers)
    response.raise_for_status()
    data = response.json()

    doctorId = data['results'][0]['id']
    doctorLastName = data['results'][0]['last_name']

    # get all patients
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

    # sort patients by birthday and no date of birth
    for patient in patients:
        if patient[u'date_of_birth'] == None:
            nodateofbirth.append(patient)
        elif patient[u'date_of_birth'][5:] == today:
            birthday_patients.append(patient)

    success = False 
    nobirthday = False 
    nocontact = False 

    if request.GET.get("hapbir"):
        if len(birthday_patients) > 0:
            for p in birthday_patients:
                if p[u'email'] != None or p[u'cell_phone'] != None:
                    # TODO: how to handle message where some patients have contact info and others don't
                    # prehaps it doesn't matter

                    # def send_email(usersEmail, usersName, doctorsName)
                    # def send_text(usersNumber, usersName, doctorsName)
                    success = True
                    if p[u'email']:
                        # try sending email first, then send text
                        # TODO: see if users have preference?
                        args = (p[u'email'], p[u'first_name'] + " " + p[u'last_name'], doctorLastName)
                        t = threading.Thread(target=send_email, args=args)
                        t.setDaemon(True)
                        t.start()
                    elif p[u'cell_phone']:
                        # making naive assumtions here with number formatting
                        # looks like default format is '(***) ***-****'
                        number = "+1"
                        for ch in p[u"cell_phone"]:
                            if ch.isdigit():
                                number += ch
            
                        if len(number) == 12:
                            args = (number, p[u'first_name'] + " " + p[u'last_name'], doctorLastName)
                            t = threading.Thread(target=send_text, args=args)
                            t.setDaemon(True)
                            t.start()
                else:
                    nocontact = True
        else:
            # no patients with birthday
            nobirthday = True 
        
        
    context = {
        'birthday_patients' : birthday_patients,
        'link' : link,
        'nobirthday' : nobirthday,
        'nocontact' : nocontact,
        'nodateofbirth' : nodateofbirth,
        'patients' : patients,
        'success' : success,
    }
    return HttpResponse(template.render(context, request))

