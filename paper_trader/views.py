from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Trade
from django.views import View
from django.views.generic import ListView
from .models import Strategy
from django.db.models import Count



def trade_list_http(request):

    all_trades = Trade.objects.all()

    template = loader.get_template("paper_trader/trade_list.html")

    context = {
        "trades": all_trades,
    }

    html_output = template.render(context, request)

    return HttpResponse(html_output)


def trade_list_render(request):

    all_trades = Trade.objects.all()

    context = {
        "trades": all_trades,
    }

    return render(request, "paper_trader/trade_list.html", context)


class StrategyListBaseView(View):
    def get(self, request):
        strategies = Strategy.objects.all()
        context = {
            "strategies": strategies,
        }
        return render(request, "paper_trader/strategy_list_base.html", context)


class StrategyListGenericView(ListView):
    model = Strategy
    template_name = "paper_trader/strategy_list_generic.html"
    context_object_name = "strategies"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            return queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get('q', '')

        context['total_strategies'] = Strategy.objects.count()

        context['rules_per_strategy'] = Strategy.objects.annotate(
            rule_count=Count('rules')
        ).order_by('-rule_count')

        context['trades_per_strategy'] = Strategy.objects.annotate(
            trade_count=Count('trades')
        ).order_by('-trade_count')

        return context