from django.contrib import admin
from django.urls import include, path

from task_blog.views import RegisterFormView, UserEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('task_blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterFormView.as_view(), name='registration'),
    path('accounts/profile/', UserEditView.as_view(), name="profile"),
]
