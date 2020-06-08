from django.shortcuts import render
from django.views.generic import View

class Base(View):
    TEMPLATE = 'client/base.html'

    def get(self, request):
        return render(request, self.TEMPLATE)