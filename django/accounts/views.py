from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer

User = get_user_model()

# 意図しない動作は、return Response でエラーコードを返すことができる

# アカウント登録
class RegisterView(APIView):
    # アカウント登録はログイン前なので、permission_classesにAllowAnyを設定する。
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        # フロントエンドから渡されるrequest.dataの中のname, email, passwordを利用してユーザーを作成
        try:
            data = request.data
            name = data['name']
            email = data['email'].lower()
            password = data['password']

            # ユーザーの存在確認
            if not User.objects.filter(email=email).exists():
                # ユーザーが存在しない場合は作成
                User.objects.create_user(
                    name=name, email=email, password=password)

                return Response(
                    {'success': 'ユーザーの作成に成功しました'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': '既に登録されているメールアドレスです'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'アカウント登録時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ユーザー情報取得
class UserView(APIView):
    # ユーザー情報取得は認証後なので、permission_classesにAllowAnyは設定しない
    # → APIアクセスにはアクセストークンが必要になる

    def get(self, request):
        try:
            # request.userからシリアライザーを通してユーザー情報を取得する
            user = request.user
            user = UserSerializer(user)

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'ユーザーの取得に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
