from django.urls import path
from .views import UserSignupView, UserLoginView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name="user-login"),
]