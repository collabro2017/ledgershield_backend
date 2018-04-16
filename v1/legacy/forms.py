from django import forms

from v1.coins.models import Coin


class TransactionForm(forms.Form):
    deposit = forms.ModelChoiceField(
        queryset=Coin.objects.all(),
        required=True,
        empty_label='Choose source coin!',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    rollback_wallet = forms.CharField(
        required=True,
        label='Your Refund Address',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    withdraw = forms.ModelChoiceField(
        queryset=Coin.objects.all(),
        required=True,
        empty_label='Choose destination coin!',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    outs = forms.CharField(widget=forms.HiddenInput({'value': 1}))

