import os

__author__ = 'padickinson'

DEBUG = True
ADMINS = frozenset([
    os.environ.get('ADMIN_EMAIL')
])