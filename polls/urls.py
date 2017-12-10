from django.conf.urls import url
from . import views
from .views import Signup, Home

urlpatterns = [
    url(r'^signup$', Signup.as_view(), name='signup'),
    url(r'^home$', Home.as_view(), name='home'),
]



