from django.urls import path
from app.dashboard.views.base import Index, Admin
from app.dashboard.views.extends import Extends

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('admin', Admin.as_view(), name='admin'),

]