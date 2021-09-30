from django.urls import path
from . import views

app_name = 'emailupdates'

urlpatterns = [
    path('signingup',views.email_subscribe, name = 'signingup'),
    path('unsigning',views.email_unsubscribe, name = 'unsigning'),
    path('banana',views.voila)

]