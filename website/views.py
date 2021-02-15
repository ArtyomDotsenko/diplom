from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm



def index(request):
    return render(request, 'website_base/base_1.html')


def register(request):
    data = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            data['form'] = form
            data['res'] = "Всё прошло успешно"
            return render(request, 'website/registration.html', data)
    else:
        form = UserCreationForm()
        data['form'] = form
        return render(request, 'website/registration.html', data)