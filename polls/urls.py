from django.conf.urls import url
from . import views
from .views import Signup, Home, Login, ValidateUsername, ValidateEmail
from django.contrib.auth import views as built_views


urlpatterns = [
    url(r'^signup$', Signup.as_view(), name='signup'),
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^home$', Home.as_view(), name='home'),
    url(r'^logout$', built_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^validate_username$', ValidateUsername.as_view(), name='validate_username'),
    url(r'^validate_email$', ValidateEmail.as_view(), name='validate_email'),

]



