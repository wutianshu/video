from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.generic import View
from app.models.auth import ClientUser
import json


def client_auth(func):
    def inner(obj, request):
        userId = request.COOKIES.get("userid")
        if not userId:
            return redirect(reverse('client_login'))
        return func(obj, request)

    return inner


class Base(View):
    TEMPLATE = 'client/client_test.html'

    @client_auth
    def get(self, request):
        return render(request, self.TEMPLATE)


class ClientUserLogin(View):
    TEMPLATE = 'client/client_login.html'

    def get(self, request):
        return render(request, self.TEMPLATE)

    def post(self, request):
        userName = request.POST.get("username")
        password = request.POST.get("password")

        user = ClientUser.get_user(username=userName, password=password)
        if user:
            userId = user.id
            response = HttpResponse("登录成功")
            print(userId)
            response.set_cookie('userid', userId)
            return response
        else:
            return redirect(reverse('client_index'))


class Test(View):

    def get(self, request):
        httpResDic = {"status": "0", "message": "记录成功"}
        httpRes = json.dumps(httpResDic, ensure_ascii=False)
        return HttpResponse(httpRes, content_type="application/json")

    def post(self, request):
        videoId = request.POST.get("videoId")
        userId = request.POST.get("userId")
        httpResDic = {"status": "0", "message": "记录成功", "info": {"videoId": videoId, "userId": userId}}
        httpRes = json.dumps(httpResDic, ensure_ascii=False)
        return HttpResponse(httpRes, content_type="application/json")
