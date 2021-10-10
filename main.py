from django.core.management import execute_from_command_line
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from pathlib import Path
import random
import string

BASE_DIR = Path(__file__).resolve().parent
VIEWS_DIR = BASE_DIR / 'views'
DEBUG = True
SECRET_KEY = 121233231
ROOT_URLCONF = __name__
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [''],
    }
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}

FORM_MESSAGES = {
    'info': 'Введите в поле ниже адрес начинающийся с http:// <b>/</b> https:// <b>/</b> ftp://',
    'danger': 'Не удалось создать короткую ссылку для адреса {url}',
    'success': 'Ссылка успешно создана!'
}


def main_page_handler(request):
    return render(request, VIEWS_DIR / 'main.html')


def validate_given_url(given_url):
    return given_url.find('https://') == 0 or given_url.find('http://') == 0 or given_url.find('ftp://') == 0


def generate_unique_hash():
    unique_hash = ''.join(random.choice(string.digits + string.ascii_lowercase) for i in range(10))
    if find_resource_by_hash(unique_hash):
        unique_hash = generate_unique_hash()
    return unique_hash


def get_short_url(original_url):
    with connection.cursor() as cur:
        cur.execute("SELECT shortcut FROM urls WHERE original=%s LIMIT 1", [original_url])
        existing_shortcut_entity = cur.fetchone()
        if existing_shortcut_entity:
            shortcut = existing_shortcut_entity[0]
        else:
            shortcut = generate_unique_hash()
            cur.execute("INSERT INTO urls (original, shortcut) VALUES (%s, %s)", [original_url, shortcut])
            cur.fetchone()

        return shortcut


def find_resource_by_hash(url_hash):
    with connection.cursor() as cur:
        cur.execute("SELECT original FROM urls WHERE shortcut=%s LIMIT 1", [url_hash])
        res = cur.fetchone()

    return res[0] if res else None


def url_shortener(request):
    if request.method == 'GET':
        message_type = 'info'
        data_for_view = {'message': True, 'message_type': message_type, 'message_text': FORM_MESSAGES[message_type]}

    elif request.method == 'POST':
        given_url = request.POST.get('url', '')
        if validate_given_url(given_url):
            shortcut = get_short_url(given_url)
            message_type = 'success'
            data_for_view = {
                'message': True,
                'message_type': message_type,
                'message_text': FORM_MESSAGES[message_type],
                'message_link': shortcut
            }

        else:
            message_type = 'danger'
            data_for_view = {
                'message': True,
                'message_type': message_type,
                'message_text': FORM_MESSAGES[message_type].format(url=given_url)
            }

    return render(request, VIEWS_DIR / 'form.html', data_for_view)


def short_url_handler(request, url_hash):
    original_url = find_resource_by_hash(url_hash)

    return redirect(original_url if original_url else '/')


urlpatterns = [
    path('', main_page_handler),
    path('url_shortener', url_shortener),
    path('su/<url_hash>', short_url_handler),
]

if __name__ == '__main__':
    execute_from_command_line()
