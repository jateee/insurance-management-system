from insu.fedha.forms import LoginForm


from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render


def login (request):

    form = LoginForm()
    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'loginForm':form}

    return render(request, 'fedha/login.html', context=context)