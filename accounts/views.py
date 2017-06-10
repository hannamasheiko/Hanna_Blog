
from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
)

from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm, UserRegisterForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        login(request,user)
        return redirect('/')
    return render(request,'accounts/form.html', {'form':form})

def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        return redirect('/')

    context = {
        'form':form,
        'title':title
    }

    return render(request, 'accounts/form.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')