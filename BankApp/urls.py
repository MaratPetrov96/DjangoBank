from django.urls import path
from . import views

urlpatterns=[
    path('transfer',views.transfer),
    path('last',views.last_trans),
    path('u_id',views.send_user_id),
    path('account',views.send_account),
    path('login',views.Login),
    path('',views.main),
    ]
