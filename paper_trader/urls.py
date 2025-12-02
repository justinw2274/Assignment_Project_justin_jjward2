from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'paper_trader'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='paper_trader:strategy_list_generic', permanent=False)),

    path('strategies/generic/', views.StrategyListGenericView.as_view(), name='strategy_list_generic'),
    path('strategies/new/fbv/', views.strategy_create_fbv, name='strategy_create_fbv'),
    #path('strategies/new/cbv/', views.StrategyCreateCBV.as_view(), name='strategy_create_cbv'),

    path('reports/', views.reports_view, name='reports'),
    path('export/csv/', views.export_strategies_csv, name='export_csv'),
    path('export/json/', views.export_strategies_json, name='export_json'),

    path('api/strategies/', views.api_strategy_list, name='api_strategy_list'),
    path('api/strategies/summary/', views.StrategySummaryApiView.as_view(), name='strategy_summary_api'),

    path('external/crypto-prices/', views.CryptoPriceView.as_view(), name='crypto_prices'),
    path('api/external/crypto-prices/', views.CryptoPriceAPIView.as_view(), name='crypto_prices_api'),

    path('charts/dashboard/', views.strategy_chart_page, name='strategy_chart_page'),
    path('charts/api_driven_chart.png', views.api_driven_chart_view, name='api_driven_chart'),
    path('api/ping/json/', views.api_ping_json, name='api_ping_json'),
    path('api/ping/text/', views.api_ping_text, name='api_ping_text'),
]
