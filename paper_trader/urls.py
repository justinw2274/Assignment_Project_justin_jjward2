from django.urls import path
from . import views

app_name = 'papertrader'

urlpatterns = [
    path('trades/http/', views.trade_list_http, name='trade_list_http'),

    path('trades/render/', views.trade_list_render, name='trade_list_render'),
]
