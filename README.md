# drchrono Hackathon

### Requirements
- [pip](https://pip.pypa.io/en/stable/)
- [python virtual env](https://packaging.python.org/installing/#creating-and-using-virtual-environments)

### Setup
``` bash
$ pip install -r requirements.txt
$ python manage.py runserver
```

`social_auth_drchrono/` contains a custom provider for [Python Social Auth](http://python-social-auth.readthedocs.io/en/latest/) that handles OAUTH for drchrono. To configure it, set these fields in your `drchrono/settings.py` file:

```
SOCIAL_AUTH_DRCHRONO_KEY
SOCIAL_AUTH_DRCHRONO_SECRET
SOCIAL_AUTH_DRCHRONO_SCOPE
LOGIN_REDIRECT_URL
```


Changes made:
- Added python social auth to connect to drchrono api, changes can be found in settings.py and views.py.
- Added functionality in views.py to pull current user and all the user's patients from drchrono api.
- Added functions send_email and send_text in utils.py to send an email using gmail and send a text using twilio respectively.
- Added twitter bootstrap alerts to show success/error messages from sending messages.
