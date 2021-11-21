import string
from django.db import connection
import random
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import UrlForm, RegisterForm
from .models import Url

User = get_user_model()


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UserEditView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = 'registration/update_user.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class HomePageView(generic.TemplateView):
    template_name = 'index.html'

#replaced from prev HW
def find_resource_by_hash(unique_hash):
    with connection.cursor() as cur:
        cur.execute("SELECT original FROM url_shortener_url WHERE shortcut=%s LIMIT 1", [unique_hash])
        res = cur.fetchone()

    return res[0] if res else None

#replaced from prev HW
def generate_unique_hash():
    unique_hash = ''.join(random.choice(string.digits + string.ascii_lowercase) for i in range(10))
    if find_resource_by_hash(unique_hash):
        unique_hash = generate_unique_hash()
    return unique_hash


class UrlCreate(LoginRequiredMixin, generic.CreateView):
    model = Url
    fields = ['original']
    template_name = 'create_shortcut.html'

    def form_valid(self, form):
        given_url = self.request.POST.get('original')
        is_url_valid = given_url.find('https://') == 0 or given_url.find('http://') == 0 or given_url.find('ftp://') == 0

        if is_url_valid:
            url = form.save(commit=False)
            # replaced from prev HW
            with connection.cursor() as cur:
                cur.execute("SELECT shortcut FROM url_shortener_url WHERE original=%s AND user_id=%s LIMIT 1", [given_url, self.request.user.id])
                existing_shortcut_entity = cur.fetchone()
                if existing_shortcut_entity:
                    shortcut = existing_shortcut_entity[0]
                else:
                    shortcut = generate_unique_hash()

                    url.user = self.request.user
                    url.shortcut = shortcut
                    url.redirect_count = 0
                    url.save()
                    self.object = url

        return HttpResponseRedirect(reverse_lazy('creation_success', args={shortcut}))


def creation_success(request, url_hash):
    context = {'url_shortcut': url_hash}

    return render(request, 'create_shortcut_success.html', context)


def short_url_handler(request, url_hash):
    entities = Url.objects.all().filter(shortcut=url_hash)[:1]
    entity = entities[0] if entities else None

    if entity:
        entity.increaseRedirection()

        return HttpResponseRedirect(entity.original)
    else:
        return HttpResponseRedirect(reverse_lazy('index'))
