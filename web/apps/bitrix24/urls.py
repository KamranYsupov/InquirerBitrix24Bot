from django.urls import path, include

from . import views

urlpatterns = [
    path('webhook/', views.bitrix_webhook, name='webhook'),
]

app_name = 'bitrix24'
