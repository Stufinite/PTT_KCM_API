from .settings import DEBUG
import urllib
p=urllib.parse.quote('udic@720')

MongoUri = {
    "DEBUG":None,
    "Production":'mongodb://udic:'+p+'@140.120.13.243:27017'
}
if DEBUG:
    uri = MongoUri['DEBUG']
else:
    uri = MongoUri['Production']


import os
from .settings import BASE_DIR

DATABASE_SETTINGS = {
    'sqlite': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    'mysql': {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': 'PTT_IP_db',
            'USER': 'j9963232q',
            'PASSWORD': 'mysqlipdb',
            'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '3306',
            'OPTIONS': {
              'autocommit': True,
              'charset': 'utf8',
            },
        }
    }
}