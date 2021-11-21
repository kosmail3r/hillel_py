from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('url_shortener', views.UrlCreate.as_view(), name='url_shortener'),
    path('creation_success/<str:url_hash>', views.creation_success, name='creation_success'),
    path('shortcut/<str:url_hash>', views.short_url_handler, name='shortcut_for_url'),
]
