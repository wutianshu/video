from django.urls import path
from app.dashboard.views.base import Index, Admin, Admin_setting, VideoHandle, FileCreat, FileModify, VideoDelete, Test
from app.dashboard.views.auth import User_login, Register, User_logout, permission

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('admin', Admin.as_view(), name='admin'),
    path('login', User_login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('logout', User_logout.as_view(), name='logout'),
    path('admin/setting', Admin_setting.as_view(), name='admin_setting'),
    path('admin/permission', permission, name='admin_permission'),

    path('video', VideoHandle.as_view(), name='video'),
    path('file/<str:videoid>', FileCreat.as_view(), name='file'),
    path('filemodify', FileModify.as_view(), name='filemodify'),
    path('video/delete/<str:videoid>', VideoDelete.as_view(), name='video_delete'),

    path('test', Test.as_view(), name='test'),

]
