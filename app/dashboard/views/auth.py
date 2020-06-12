from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password



class User_login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        return render(request, self.TEMPLATE)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            data = {"error": "用户名不存在"}
            return render(request, self.TEMPLATE, data)
        user = authenticate(username=username, password=password)
        if not user:
            data = {"error": "密码错误"}
            return render(request, self.TEMPLATE, data)
        login(request, user)
        return redirect(reverse("index"))


class User_logout(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        logout(request)
        return render(request, self.TEMPLATE)


class Register(View):
    TEMPLATE = 'dashboard/auth/register.html'

    def get(self, request):
        return render(request, self.TEMPLATE)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        chk_pwd = request.POST.get("check_password")
        if not username:
            data = {'error': '用户名不能为空'}
            return render(request, self.TEMPLATE, data)
        if not password:
            data = {'error': '密码不能为空'}
            return render(request, self.TEMPLATE, data)
        if password != chk_pwd:
            data = {'error': '两次密码不一致'}
            return render(request, self.TEMPLATE, data)
        user = User.objects.filter(username=username).exists()
        if user:
            data = {'error': '用户名已存在'}
            return render(request, self.TEMPLATE, data)

        User.objects.create(username=username, password=make_password(password))
        return redirect(reverse('login'))

