from django.contrib import admin
from django.urls import include, path

from url_shortener.views import RegisterFormView, UserEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('url_shortener.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterFormView.as_view(), name='registration'),
    # path('accounts/profile/', UserEditView.as_view(), name="profile"),
]
