import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from io import BytesIO
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.db.models import Count
from .models import Trade, Strategy
from django.urls import reverse
from .forms import StrategyForm


def trade_list_http(request):
    all_trades = Trade.objects.all()
    template = loader.get_template("paper_trader/trade_list.html")
    context = {"trades": all_trades}
    html_output = template.render(context, request)
    return HttpResponse(html_output)


def trade_list_render(request):
    all_trades = Trade.objects.all()
    context = {"trades": all_trades}
    return render(request, "paper_trader/trade_list.html", context)


class StrategyListBaseView(View):
    def get(self, request):
        strategies = Strategy.objects.all()
        context = {"strategies": strategies}
        return render(request, "paper_trader/strategy_list_base.html", context)


class StrategyListGenericView(ListView):
    model = Strategy
    template_name = "paper_trader/strategy_list_generic.html"
    context_object_name = "strategies"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["total_strategies"] = Strategy.objects.count()
        context["rules_per_strategy"] = (
            Strategy.objects.annotate(rule_count=Count("rules"))
            .order_by("-rule_count")
        )
        context["trades_per_strategy"] = (
            Strategy.objects.annotate(trade_count=Count("trades"))
            .order_by("-trade_count")
        )
        return context


def strategy_rules_chart(request):
    strategy_data = (
        Strategy.objects.annotate(rule_count=Count("rules"))
        .order_by("name")
    )

    strategy_names = [s.name for s in strategy_data]
    rule_counts = [s.rule_count for s in strategy_data]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(strategy_names, rule_counts, color="#1976d2")
    ax.set_title("Number of Rules per Strategy")
    ax.set_xlabel("Number of Rules")
    ax.set_ylabel("Strategy")
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type="image/png")


def strategy_create_fbv(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('paper_trader:strategy_list_generic'))
    else:
        form = StrategyForm()

    return render(request, 'paper_trader/strategy_form_fbv.html', {
        'form': form,
        'view_type': 'Function-Based View'
    })