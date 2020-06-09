from django.shortcuts import render
from django.views.generic import View


class Index(View):
    TEMPLATE = 'dashboard/index.html'

    def get(self, request):
        return render(request, self.TEMPLATE)


class Admin(View):
    TEMPLATE = 'dashboard/admin.html'

    def get(self, request):
        return render(request, self.TEMPLATE)
