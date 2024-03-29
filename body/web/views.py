from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from rest_framework.authtoken.models import Token


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = Token.objects.get(user=user)
            user = token.user

            user_data = {
                'username': user.username,
                'email': user.email,
                'password': user.password
            }
            messages.success(request, 'You are now logged in')
            return render(request, 'home.html', {'token': token.key, 'user_data': user_data})
        else:
            messages.success(request, 'Invalid credentials')
            return redirect('home')
    else:
        return render(request, 'home.html', {})


def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'You are now logged in')
            user_data = {
                'username': user.username,
                'email': user.email,
                'password': user.password
            }
            return render(request, 'home.html', {'token': token.key, 'user_data': user_data})
        else:
            messages.success(request, 'Unsuccessful sign up. Invalid information.')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {"form": form})

    return render(request, 'signup.html', {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')


def change_name(request):
    if request.method == 'POST':
        if 'new_name' in request.POST and 'token' in request.POST:
            new_name = request.POST['new_name']
            token_key = request.POST['token']
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                user.username = new_name
                user.save()
                messages.success(request, 'Username changed successfully')
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'password': user.password
                }
                user = authenticate(request, username=user_data['username'], password=user_data['password'])
                login(request, user)
                return render(request, 'home.html', {'token': token.key, 'user_data': user_data})
            except Token.DoesNotExist:
                messages.error(request, 'Token does not exist')
        else:
            messages.error(request, 'New name or token not provided')
        # return redirect('home')
    else:
        return render(request, 'change_name.html')


def change_email(request):
    if request.method == 'POST':
        if 'new_email' in request.POST and 'token' in request.POST:
            new_email = request.POST['new_email']
            token_key = request.POST['token']
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                user.email = new_email
                user.save()
                messages.success(request, 'Email changed successfully')
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'password': user.password
                }
                return render(request, 'home.html', {'token': token.key, 'user_data': user_data})
            except Token.DoesNotExist:
                messages.error(request, 'Token does not exist')
        else:
            messages.error(request, 'New name or token not provided')
        # return redirect('home')
    else:
        return render(request, 'change_email.html')


def change_password(request):
    if request.method == 'POST':
        if 'new_password' in request.POST and 'token' in request.POST:
            new_password = request.POST['new_password']
            token_key = request.POST['token']
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully')
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'password': user.password
                }
                return render(request, 'home.html', {'token': token.key, 'user_data': user_data})
            except Token.DoesNotExist:
                messages.error(request, 'Token does not exist')
        else:
            messages.error(request, 'New name or token not provided')
        # return redirect('home')
    else:
        return render(request, 'change_password.html')


def delete_account(request):
    if request.method == 'POST':
        if 'token' in request.POST:
            token_key = request.POST['token']
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                user.delete()
                messages.success(request, 'Account deleted successfully')
                return redirect('home')
            except Token.DoesNotExist:
                messages.error(request, 'Token does not exist')
        else:
            messages.error(request, 'Token not provided')
    else:
        return render(request, 'delete_account.html')
