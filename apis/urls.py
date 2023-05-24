# basic URL Configurations
from django.urls import path
from . import views

app_name = 'apis'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_pdf/', views.sign_pdf, name='sign_pdf'),
    path('relay-trello-webhook/', views.relay_trello_webhook, name='relay_trello_webhook'),
    path('jaybro-invoice/', views.create_jaybro_invoice, name='create_invoice'),
]