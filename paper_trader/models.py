from django.db import models


class Strategy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Strategies"

    def __str__(self):
        return self.name


class Rule(models.Model):
    INDICATOR_CHOICES = [
        ('RSI', 'Relative Strength Index'),
        ('SMA', 'Simple Moving Average Crossover'),
        ('MACD', 'MACD Signal Cross'),
    ]
    OPERATOR_CHOICES = [
        ('gt', 'is greater than'),
        ('lt', 'is less than'),
        ('cross_above', 'crosses above'),
    ]

    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name='rules')

    indicator = models.CharField(max_length=20, choices=INDICATOR_CHOICES)
    operator = models.CharField(max_length=20, choices=OPERATOR_CHOICES)
    value = models.FloatField(help_text="The value to compare the indicator against.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['strategy', 'indicator', 'operator', 'value'],
                                    name='unique_rule_per_strategy')
        ]
        ordering = ['id']

    def __str__(self):
        return f"IF {self.get_indicator_display()} {self.get_operator_display()} {self.value}"


class Trade(models.Model):
    ACTION_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell')
    ]

    strategy = models.ForeignKey(Strategy, on_delete=models.PROTECT, related_name='trades')

    symbol = models.CharField(max_length=10)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    trade_date = models.DateTimeField()

    class Meta:
        ordering = ['-trade_date']

    def __str__(self):
        return f"{self.action} {self.quantity} {self.symbol} @ {self.price} on {self.trade_date.strftime('%Y-%m-%d')}"
