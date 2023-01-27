from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserCreationForm, NewUserChangeForm, PhoneValForm
from django.utils.translation import gettext as _

def login_user(request):
    if request.method == 'POST':
        try:
            def password_generator(username):
                dic = {'1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i', '0': 'j', ' ': 'k'}
                password = []
                for i in str(username):
                    password.append(dic[i])
                return "".join(password)
            username = request.POST['phone_number']
            password = password_generator(username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, (_('You have logged in successfully')))
                return redirect('appointments:home')
            else:
                print("User is None")
                messages.error(request, (_('Phone number is not registered')))
                return redirect('authenticate:login')
        except:
            context = {}
            messages.error(request, (_('Invalid phone number')))
            return render(request, 'authenticate/login.html', context)
    else:
        context = {}
        return render(request, 'authenticate/login.html', context)

@login_required(login_url='/authenticate/login/')
def logout_user(request):
    logout(request)
    messages.success(request, (_('You were logged out')))
    return redirect('authenticate:login')

def register_user(request):
    if request.method == 'POST':
        form = PhoneValForm(request.POST)
        if form.is_valid():
            def password_generator(username):
                dic = {'1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i', '0': 'j', ' ': 'k'}
                password = []
                for i in str(username):
                    password.append(dic[i])
                return "".join(password)
            phone_number = request.POST['phone_number']
            username = phone_number
            password1 = password_generator(phone_number)
            password2 = password_generator(phone_number)
            post = {'username': username, 'phone_number': phone_number, 'password1': password1, 'password2': password2}
            form_2 = NewUserCreationForm(post)
            if form_2.is_valid():
                form_2.save()
                username = form_2.cleaned_data['username']
                password = form_2.cleaned_data['password2']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, (_('Registration successful')))
                return redirect('appointments:home')
            else:
                print("User is not None")
                messages.error(request, (form_2.errors))
                return redirect('authenticate:register')
        else:
            messages.error(request, (_('Invalid phone number, enter a +10 digit number with no spaces in between')))
            return redirect('authenticate:register')
    else:
        form = PhoneValForm()
        context = {'form': form}
        return render(request, 'authenticate/register.html', context)

# def register_user(request):
    if request.method == 'POST':
        def password_generator(username):
            dic = {'1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i', '0': 'j', }
            password = []
            for i in str(username):
                password.append(dic[i])
            return "".join(password)
        username = request.POST['phone_number']
        password1 = password_generator(username)
        password2 = password_generator(username)
        post = {'username': username, 'password1': password1, 'password2': password2}
        form = UserCreationForm(post)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registration successful'))
            return redirect('appointments:home')
        else:
            print('form is not valid')
    else:
        form = UserCreationForm()
            
    context = {'form': form}
    return render(request, 'authenticate/register.html', context)