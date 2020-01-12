from django.conf.urls import url, include
from . import views
from django.conf import settings
app_name = 'home'

urlpatterns = [
    url(r'^$', views.menu, name='menu'),
    url(r'^allcontent/(?P<allcontent_id>\D+)/$', views.allcontent, name='allcontent'),
    url(r'^data/(?P<job_name>\D+)/$', views.data, name='data'),
    url(r'^home/aboutus/$', views.aboutus, name='aboutus'),
    url(r'^home/signup/$', views.signup, name='signup'),
    url(r'^home/login/$', views.login, name='login'),
    url(r'^home/search/$', views.search, name='search'),
    url(r'^home/logout/$', views.logout, name='logout'),
    url(r'^home/profile/$', views.profile, name='profile'),
    url(r'^practice/(?P<practice_type>\D+)/(?P<category_name>\D+)/(?P<filterby>\D+)/$', views.practice, name='practice'),
    url(r'^paper/(?P<practice_type>\D+)/(?P<category_name>\D+)/(?P<filterby>\D+)/(?P<paper_name>\D+)/(?P<time>\d+)/$', views.paper, name='paper'),
    url(r'^result/(?P<practice_type>\D+)/(?P<category_name>\D+)/(?P<filterby>\D+)/(?P<paper_name>\D+)/(?P<time>\d+)/$', views.result, name='result'),
    url(r'^home/contactus/$', views.contactus, name='contactus'),
]