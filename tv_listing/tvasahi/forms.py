from django import forms
from .models import Comment, Category, CustomUser
from django.contrib.auth.forms import UserCreationForm


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)


class SearchForm(forms.Form):
    keyword = forms.CharField(label='キーワード', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='カテゴリー', required=False,
                                      empty_label='選択してください')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'address', 'favorite_category')


class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'favorite_category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
