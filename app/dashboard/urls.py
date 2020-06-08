from django.urls import path
from app.dashboard.views.base import Base

urlpatterns = [
    path('base', Base.as_view(), name='base'),

]