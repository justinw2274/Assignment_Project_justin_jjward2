from django import forms
from .models import Strategy

class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name) < 5:
            raise forms.ValidationError("Strategy name must be at least 5 characters long.")
        return name
