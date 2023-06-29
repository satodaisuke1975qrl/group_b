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
        fields = ('username', 'email', 'address', 'favorite_category', 'icon')
        error_messages = {
            'username': {
                'required': "ユーザー名を入力してください。",
            },
            'password1': {
                'required': "パスワードを入力してください。",
            },
            'password2': {
                'required': "パスワードを入力してください。",
            },
            'email': {
                'required': "メールアドレスを入力してください。",
                'invalid': "メールアドレスの形式が不適切です。",
                'unique': "このメールアドレスは既に使用されています。"
            },
            'address': {
                'required': "住所を入力してください。",
            },
            'favorite_category': {
                'required': "カテゴリーを入力してください。",
            },

        }


class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'address', 'favorite_category', 'icon')
        error_messages = {
            'username': {
                'required': "ユーザー名を入力してください。",
            },
            'email': {
                'required': "メールアドレスを入力してください。",
                'invalid': "メールアドレスの形式が不適切です。",
                'unique': "このメールアドレスは既に使用されています。"
            },
            'address': {
                'required': "住所を入力してください。",
            },
            'favorite_category': {
                'required': "カテゴリーを入力してください。",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # def clean_username(self):
    #     username = self.cleaned_data['username']

