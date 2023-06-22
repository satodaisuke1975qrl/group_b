from django.contrib import admin

# Register your models here.
from .models import Category, Date, Tv, Comment, CustomUser


admin.site.register(Category)
admin.site.register(Date)
admin.site.register(Tv)
admin.site.register(Comment)
admin.site.register(CustomUser)