import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('NAME_BD'),
        'USER': config('USER_BD'),
        'PASSWORD': config('PASSWORD_BD'),
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('NAME_BD'),
        'USER': config('USER_BD'),
        'PASSWORD': config('PASSWORD_BD'),
        'HOST': 'localhost',
        'PORT': '5432'
    }
}