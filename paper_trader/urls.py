from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'paper_trader'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='paper_trader:strategy_list_generic', permanent=True)),

    path('trades/http/', views.trade_list_http, name='trade_list_http'),

    path('trades/render/', views.trade_list_render, name='trade_list_render'),

    path('strategies/base/', views.StrategyListBaseView.as_view(), name='strategy_list_base'),

    path('strategies/generic/', views.StrategyListGenericView.as_view(), name='strategy_list_generic'),

    path('strategies/generic/', views.StrategyListGenericView.as_view(), name='strategy_list_generic'),

    path('charts/strategy_rules.png', views.strategy_rules_chart, name='strategy_rules_chart'),

    path('strategies/new/fbv/', views.strategy_create_fbv, name='strategy_create_fbv'),

    path('strategies/new/cbv/', views.StrategyCreateCBV.as_view(), name='strategy_create_cbv'),

    path('api/strategies/', views.api_strategy_list, name='api_strategy_list'),

    path('api/strategies/summary/', views.StrategySummaryApiView.as_view(), name='strategy_summary_api'),

    path('api/ping/json/', views.api_ping_json, name='api_ping_json'),

    path('api/ping/text/', views.api_ping_text, name='api_ping_text'),

    path('charts/dashboard/', views.strategy_chart_page, name='strategy_chart_page'),

    path('charts/api_driven_chart.png', views.api_driven_chart_view, name='api_driven_chart'),

    path('external/crypto-prices/', views.CryptoPriceView.as_view(), name='crypto_prices'),

    path('api/external/crypto-prices/', views.CryptoPriceAPIView.as_view(), name='crypto_prices_api'),
]
