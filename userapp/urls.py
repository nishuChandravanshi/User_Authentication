from django.conf.urls import url
from django.urls import path
from userapp import views


#TEMPLATES URLS!
app_name='userapp'
# appname variable

urlpatterns=[
# url(r'^register/$',views.register,name='register'),
path('register/',views.register,name='register'),
path('user_login/',views.user_login,name='user_login'),

]
