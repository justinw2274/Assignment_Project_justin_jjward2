import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import urllib.request
import io
import requests

from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.db.models import Count
from .models import Trade, Strategy
from django.urls import reverse
from .forms import StrategyForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import SignUpForm


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

class StrategyCreateCBV(CreateView):
    model = Strategy
    form_class = StrategyForm
    template_name = 'paper_trader/strategy_form_cbv.html'
    success_url = reverse_lazy('paper_trader:strategy_list_generic')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'Class-Based View'
        return context


def api_strategy_list(request):
    strategies = list(Strategy.objects.values('id', 'name', 'description'))
    data = {
        'count': len(strategies),
        'results': strategies,
    }
    return JsonResponse(data)


class StrategySummaryApiView(View):
    def get(self, request, *args, **kwargs):
        summary_data = list(Strategy.objects.annotate(
            rule_count=Count('rules')
        ).values('name', 'rule_count'))

        return JsonResponse(summary_data, safe=False)


def api_ping_json(request):
    return JsonResponse({'status': 'ok', 'source': 'JSON'})


def api_ping_text(request):
    return HttpResponse('status: ok, source: Plain Text', content_type='text/plain')


def api_driven_chart_view(request):
    api_url = request.build_absolute_uri(reverse('paper_trader:strategy_summary_api'))
    with urllib.request.urlopen(api_url) as response:
        api_data = json.load(response)

    strategy_names = [item['name'] for item in api_data]
    rule_counts = [item['rule_count'] for item in api_data]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(strategy_names, rule_counts, color='#004080')

    ax.set_xlabel('Number of Rules')
    ax.set_title('Strategy Complexity (Rules per Strategy)')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    return HttpResponse(buf.getvalue(), content_type='image/png')

def strategy_chart_page(request):
    return render(request, 'paper_trader/chart_page.html')


class CryptoPriceView(View):
    API_URL = "https://api.coingecko.com/api/v3/simple/price"
    def get(self, request, *args, **kwargs):
        crypto_ids = request.GET.get('ids', 'bitcoin,ethereum,dogecoin')
        params = {
            'ids': crypto_ids,
            'vs_currencies': 'usd',
        }
        try:
            response = requests.get(self.API_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            cleaned_data = [
                {'coin': coin, 'price_usd': prices.get('usd', 'N/A')}
                for coin, prices in data.items()
            ]
            context = {
                'ok': True,
                'data': cleaned_data,
                'search_query': crypto_ids,
            }
            return render(request, 'paper_trader/crypto_prices.html', context)
        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching data from CoinGecko API: {e}"
            context = {
                'ok': False,
                'error': error_message,
                'search_query': crypto_ids,
            }
            return render(request, 'paper_trader/crypto_prices.html', context)


class CryptoPriceAPIView(View):
    API_URL = "https://api.coingecko.com/api/v3/simple/price"

    def get(self, request, *args, **kwargs):
        crypto_ids = request.GET.get('ids', 'bitcoin,ethereum,dogecoin')

        params = {
            'ids': crypto_ids,
            'vs_currencies': 'usd',
        }

        try:
            response = requests.get(self.API_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            cleaned_data = [
                {'coin': coin, 'price_usd': prices.get('usd', 'N/A')}
                for coin, prices in data.items()
            ]

            return JsonResponse({
                'ok': True,
                'count': len(cleaned_data),
                'results': cleaned_data
            })

        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'ok': False,
                'error': str(e)
            }, status=502)



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            login(request, user)
            return redirect('paper_trader:strategy_list_generic')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})