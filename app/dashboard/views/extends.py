from django.shortcuts import render
from django.views.generic import View

class Extends(View):
    TEMPLATE = 'dashboard/extends.html'
    def get(self,request):
        return render(request, self.TEMPLATE)