from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from projBuzzer.forms import LoginForm
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
app_name = 'buzzer'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^student/',  include('student.urls')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^login/$', views.login, name='login'),
    url(r'^buzzer/', include('buzzer.urls')),
    url(r'^logout/$', views.logout,name='logout'),
    url(r'^$', views.login, name='login'),
        #name='index'),url(r'^$', views.index, name='index'),
    #    (r"^$", direct_to_template, {"template": "index.html"})

    #url(r'^admin_tools/', include('admin_tools.urls')),

 #url(r'^login/$', views.login, {'template_name': 'login.html','authentication_form': LoginForm},name='login'),
#    url(r'^logout/$', views.logout,{'next_page': '/login'},name='logout'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
