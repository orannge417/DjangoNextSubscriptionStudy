from django.contrib import admin
from django.contrib.auth import get_user_model

# ユーザーを管理画面で操作できるように

User = get_user_model()

admin.site.register(User)
