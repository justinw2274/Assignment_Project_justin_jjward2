from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Trade


def trade_list_http(request):

    all_trades = Trade.objects.all()

    template = loader.get_template("papertrader/trade_list.html")

    context = {
        "trades": all_trades,
    }

    return HttpResponse(template.render(context, request))


def trade_list_render(request):

    all_trades = Trade.objects.all()

    context = {
        "trades": all_trades,
    }

    return render(request, "papertrader/trade_list.html", context)
