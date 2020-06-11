from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


class Index(View):
    TEMPLATE = 'dashboard/index.html'

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user = str(request.user)
        data = {"user": user}
        return render(request, self.TEMPLATE, data)


class Admin(View):
    TEMPLATE = 'dashboard/admin.html'
    TEMPLATE_PERMISSION = 'dashboard/auth/permission.html'

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        if request.user.is_superuser:
            username = request.GET.get("username", "")
            page = request.GET.get("page", 1)
            page = int(page)
            if username:
                users = User.objects.filter(username__contains=username).order_by('id')
            else:
                users = User.objects.all().order_by('id')
            total_users = users.count()
            p = Paginator(users, 10)
            current_page = p.get_page(page)
            users = current_page.object_list
            total_page = p.num_pages
            return render(request, self.TEMPLATE,
                          {"users": users, "total_page": total_page, "total_users": total_users, "current_page": page})
        else:
            return render(request, self.TEMPLATE_PERMISSION)


class User_login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        return render(request, self.TEMPLATE)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
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


class Admin_setting(View):
    def get(self, request):
        seeting = request.GET.get("setting")
        username = request.GET.get("username")
        user = User.objects.get(username=username)
        if seeting == 'on':
            user.is_superuser = True
        elif seeting == 'off':
            user.is_superuser = False
        user.save()
        return redirect(reverse('admin'))
