from django import forms
from .models import Goods


class SearchForm(forms.Form):
    keyword = forms.CharField(label='キーワード', required=False)
