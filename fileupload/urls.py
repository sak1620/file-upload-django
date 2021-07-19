"""fileupload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from user import views as u_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import handler400,handler500

urlpatterns = [
    path('', u_views.vw_login_user, name="main_login"),
    path('admin/', admin.site.urls),
    re_path('user/', include('user.urls')),
    path('login/', u_views.vw_login_user, name="main_login"),
    path('logout/', u_views.vw_log, name="logout"),

    re_path(r'^password-reset/$', auth_views.PasswordResetView.as_view(), name="password_reset"),
    re_path(r'^password-reset/done/$', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    re_path(r'^password-reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = u_views.handler404
handler500 = u_views.handler404