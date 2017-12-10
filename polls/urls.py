from django.conf.urls import url
from . import views
from .views import Signup, Home, Login
from django.contrib.auth import views as built_views


urlpatterns = [
    url(r'^signup$', Signup.as_view(), name='signup'),
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^home$', Home.as_view(), name='home'),
    url(r'^logout$', built_views.logout, {'next_page': 'login'}, name='logout'),

]



