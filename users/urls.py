"""Posts URLS."""
#path
from typing import Generic
from django.urls import path
#Views
from users import views
from django.views.generic import TemplateView

urlpatterns=[
    path(
        route='profile/<str:username>/',
        view=views.UserDatailView.as_view(),
        name='detail'
    ),

    path(
        route='login/',
        view= views.login_view,
        name='login'
    ),

    path(
        route='logout/',
        view= views.logout_view,
        name='logout'
    ),

    path(
        route='signup/',
        view= views.signup, 
        name='signup'
    ),

    path(
        route='me/profile',
        view= views.update_profile,
        name='update'
    ),
]