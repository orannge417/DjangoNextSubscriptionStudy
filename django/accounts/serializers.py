# クエリセットやモデルインスタンスのような複雑なデータを、Json 形式のフォーマットに変換する

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')
