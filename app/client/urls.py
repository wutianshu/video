from django.urls import path

from app.client.views.base import ClientUserLogin, Base,Test

urlpatterns = [
    # path('base/', Base.as_view(), name='base'),
    path('', Base.as_view(), name='client_index'),
    path('login', ClientUserLogin.as_view(), name='client_login'),
    path('test', Test.as_view(), name='client_login'),
]
