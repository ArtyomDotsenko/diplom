from django.shortcuts import render


def index(request):
    return render(request, 'website_base/base_1.html')
