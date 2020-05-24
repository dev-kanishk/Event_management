from django.urls import path
from . import views

urlpatterns = [
    path("signUp/",views.signup,name="signup"),
    path("login/",views.user_login,name="user_login"),
    path("logout/",views.user_logout,name="user_logout"),
    path("home/",views.home,name="home"),
    path("event/",views.event,name="event"),
    path("search_event/",views.search_event,name="search_event"),

]
