from django.urls import path
from .views      import (SignUpView,
                         SignInView,
                         KakaoView,
                         ProfileView)

urlpatterns = [
    path('sign_up',     SignUpView.as_view()),
    path('sign_in',     SignInView.as_view()),
    path('kakao_login', KakaoView.as_view()),
    path('my_info',     ProfileView.as_view())
]
