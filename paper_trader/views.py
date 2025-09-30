from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Trade


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
