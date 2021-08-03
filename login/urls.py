from django.urls import path

from . import views

#app_name= 'login'

urlpatterns = [
    path('',views.home, name="home"),
    path('profile',views.profile, name="profile"),
    path('register',views.register, name="register"),
    path('forgot',views.forgot, name="forgot"),
    path('login',views.login, name="login"),
    path('edit',views.edit, name="edit"),
    path('globe',views.globe, name="globe"),
    path('simple_upload',views.simple_upload, name="simple_upload"),
    path('otp',views.otp, name="otp"),
    path('reset',views.reset, name="reset"),
    path('logout',views.logout, name="logout"),
    path('contin',views.contin, name="contin"),
    path('add_friend',views.add_friend, name="add_friend"),
    path('edit_dp',views.edit_dp, name="edit_dp"),
    path('contin2',views.contin2, name="contin2"),
    path('edit_upload',views.edit_upload, name="edit_upload"),
    path('addpostpic',views.addpostpic, name="addpostpic"),
    path('addpost',views.addpost, name="addpost"),
    path('friend',views.friend, name="friend"),
    path('chatbox',views.chatbox, name="chatbox"),
    path('follow_g',views.follow_g, name="follow_g"),
    path('follow_r',views.follow_r, name="follow_r"),
    path('home1',views.home1, name="home1"),
]   