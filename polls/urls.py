from django.conf.urls import url
from . import views
from django.contrib.auth import views as built_views

"""
ABOUT BASE64
1.convert all letter into their ascii value (a = 97)
2.convert ascii value in binary no. in eight bit pair (97 ->  01100001)
3.concatenate all binary no.
4.take pair of six
5.then convert decimal then letter and we get final number
ref ->  https://code.tutsplus.com/tutorials/base64-encoding-and-decoding-using-python--cms-25588
"""


urlpatterns = [
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^logout/$', built_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^validate_username/$', views.ValidateUsername.as_view(), name='validate_username'),
    url(r'^validate_email/$', views.ValidateEmail.as_view(), name='validate_email'),
    # first part is user_id in base 36 second part is token where one is 36base string and other is 20 length hash key
    url(r'^activate_user/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.Activate.as_view(), name='activate'),
    # url(r'^home/(?P<username>\w+)/edit/$', CreateProfile.as_view(), name='create_profile'),
    url(r'^home/(?P<pk>\d+)/edit_again/$', views.UpdateProfile.as_view(), name='update_profile'),
    url(r'^about/(?P<username>\w+)/$', views.About.as_view(), name='about_user'),
    url(r'^learn/$', views.learn, name='learn'),


]




