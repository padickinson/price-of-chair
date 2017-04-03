import os

__author__ = 'padickinson'


COLLECTION="alerts"
ALERT_TIMEOUT = 10

#   Note: these are stored as environment variables in Heroku
URL = 'https://api.mailgun.net/v3/sandbox3c05ecf70aba4cc99ed8d0621a82cdf2.mailgun.org/messages'
API_KEY = 'key-caad8cb17667ec09b58641648bf3adc0'
FROM = 'Postmaster Mailgun Sandbox <postmaster@sandbox3c05ecf70aba4cc99ed8d0621a82cdf2.mailgun.org>'
