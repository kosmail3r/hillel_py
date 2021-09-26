import this
import importlib
from importlib import util
from random import choice

from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path

settings.configure(
    DEBUG=True,
    SECRET_KEY=121233231,
    ROOT_URLCONF=__name__,
)

text = ''.join(this.d.get(c, c) for c in this.s)
title, _, *quotes = text.splitlines()

TEMPLATE = """
<!DOCTYPE html>
<html>
 <head>
  <title>{title}</title>
 </head>
 <body>
   <p>{message}</p>
 </body>
</html>
"""

LINK_TEMPLATE = "<a href='/doc/{mod_name}/{object_name}'>{object_name}</a></br>"


def get_module_by_name(module_name):
    return importlib.import_module(module_name) if importlib.util.find_spec(module_name) else None


def handler(request):
    return HttpResponse(TEMPLATE.format(title=title, message=choice(quotes)))


def mod_handler(request, module_name):
    module = get_module_by_name(module_name)
    if module is not None:
        ans = [LINK_TEMPLATE.format(mod_name=module_name, object_name=elem) for elem in dir(module)]
        template_body = ''.join(ans)
        http_code = 200
    else:
        template_body = 'Undefined module =('
        http_code = 404

    return HttpResponse(TEMPLATE.format(title='The list of module ' + module_name, message=template_body),
                        status=http_code)


def object_handler(request, module_name, object_name):
    module = get_module_by_name(module_name)
    http_code = 404

    if module is not None:
        if hasattr(module, object_name):
            explanation = getattr(module, object_name).__doc__
            http_code = 200
        else:
            explanation = "Module '{}' has no attribute '{}'".format(module_name, object_name)
    else:
        explanation = 'Undefined module =('

    return HttpResponse(explanation, content_type="text/plain", status=http_code)


urlpatterns = [
    path('', handler),
    path('doc/<module_name>', mod_handler),
    path('doc/<module_name>/<object_name>', object_handler),
]

if __name__ == '__main__':
    execute_from_command_line()
