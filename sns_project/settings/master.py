from .base import *

DEBUG = True

ADMINS = (
    ('Paulo Cesar Cassiano Pereira', 'paulo.pereira@resourceit.com'),
)

ALLOWED_HOSTS = ['*']

# TODO: Configurar aqui a Base de Dados de Producao
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'sns30',
        'USER': 'usr_sns@ambev-sns-non-prod',
        'PASSWORD': 'z77kNqqs8GFCZv7S',
        'HOST': 'ambev-sns-non-prod.mysql.database.azure.com',
        'PORT': '3306',
    }
}