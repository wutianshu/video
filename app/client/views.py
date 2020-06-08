from django.shortcuts import render
from django.views.generic import View

class Home(View):
    TEMPLATE = '1.html'
    def get(self,request):
        return render(request, self.TEMPLATE)