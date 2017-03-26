import os

__author__ = 'padickinson'


COLLECTION="alerts"
ALERT_TIMEOUT = 10

#   Note: these are stored as environment variables in Heroku
URL = os.environ.get('MAILGUN_URL')
API_KEY = os.environ.get('MAILGUN_API_KEY')
FROM = os.environ.get('MAILGUN_FROM')
