# group_b

## How to use (動かし方)

```
(仮想環境を有効化する)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```


その後、 http://127.0.0.1:8000 にブラウザでアクセスしてください。

## 名前

```
・HTML
tv_list.html : 番組一覧
tv_detail.html: : 詳細画面
tv_search.html : 検索画面

comment_create.html : 
comment_update.html : 
コメントの削除はhtmlではなくJSのポップアップにしたい

base.html : 遷移後も変えたくないもの（背景のCSSとか）はここで！

・tvasahi/forms.py
CommentCreateForm

CommentUpdateForm

SearchForm
    keyword
    category

```

