from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.models import User
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
