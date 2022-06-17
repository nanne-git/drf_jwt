from django.urls import path, include
from .views import UserRegister, UserLogin, GetUserData, ChangePassword
urlpatterns = [
    path("reg", UserRegister.as_view(), name="register"),
    path("login", UserLogin.as_view(), name="login"),
    path('getdata', GetUserData.as_view(), name="getdata"),
    path("changepassword", ChangePassword.as_view(), name="changepassword"),
]
