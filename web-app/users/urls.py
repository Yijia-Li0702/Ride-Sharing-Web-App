
from django.conf.urls import url
from django.urls import path

from.import views

urlpatterns=[
    url('register/',views.RegisterView.as_view()),
    url('checkUsername/$', views.CheckUsernameView.as_view()),
    url('login/', views.LoginView.as_view()),
    url('isExist/', views.existView),
    url('logout/', views.LogoutView),
##################################################
    url('only/', views.onlyemailView),
    
    path('<int:user_id>/userInfo/', views.userInfo),

]
