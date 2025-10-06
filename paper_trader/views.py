from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Trade
from django.views import View
from django.views.generic import ListView
from .models import Strategy


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