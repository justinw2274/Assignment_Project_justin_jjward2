from django.urls import path
from . import views

app_name = 'paper_trader'

urlpatterns = [
    path('trades/http/', views.trade_list_http, name='trade_list_http'),

    path('trades/render/', views.trade_list_render, name='trade_list_render'),

    path('strategies/base/', views.StrategyListBaseView.as_view(), name='strategy_list_base'),

    path('strategies/generic/', views.StrategyListGenericView.as_view(), name='strategy_list_generic'),

    path('strategies/generic/', views.StrategyListGenericView.as_view(), name='strategy_list_generic'),

    path('charts/strategy_rules.png', views.strategy_rules_chart, name='strategy_rules_chart'),

    path('strategies/new/fbv/', views.strategy_create_fbv, name='strategy_create_fbv'),

    path('strategies/new/cbv/', views.StrategyCreateCBV.as_view(), name='strategy_create_cbv'),
]
