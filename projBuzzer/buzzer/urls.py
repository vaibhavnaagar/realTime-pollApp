from django.conf.urls import url
from buzzer import views
app_name = 'buzzer'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'quiz/(?P<quiz_id>[0-9]+)$', views.display_quiz, name='quiz'),
    url(r'vote/(?P<quiz_id>[0-9]+)$', views.vote, name='vote'),
    url(r'results/(?P<quiz_id>[0-9]+)$', views.results, name='results'),
    url(r'thanks/(?P<quiz_id>[0-9]+)$', views.thanks, name='thanks'),
    url(r'quiz/$', views.quiz, name='quiz_redirect'),
    url(r'publish/(?P<quiz_id>[0-9]+)$', views.publish, name='publish'),
    url(r'unPublish/(?P<quiz_id>[0-9]+)$', views.unpublish, name='unpublish'),
    url(r'clear/(?P<quiz_id>[0-9]+)$', views.clear, name='clear'),


]
