from django.urls import path
from app.client.views import Home

urlpatterns = [
    path('home/', Home.as_view(), name='home'),
]