from django import forms
from .models import Comment, Category, CustomUser
from django.contrib.auth.forms import UserCreationForm


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("user_name", "comment",)


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("user_name", "comment",)


class SearchForm(forms.Form):
    keyword = forms.CharField(label='キーワード', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='カテゴリー', required=False,
                                      empty_label='選択してください')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'favorite_category')
