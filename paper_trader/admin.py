from django.contrib import admin
from .models import Strategy, Rule, Trade

class RuleInline(admin.TabularInline):
    model = Rule
    extra = 1 # Show one extra blank rule form by default

@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    inlines = [RuleInline] # Allows adding rules directly when creating/editing a strategy

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'symbol', 'action', 'price', 'quantity', 'trade_date')
    list_filter = ('strategy', 'symbol', 'action')
    search_fields = ('symbol',)
