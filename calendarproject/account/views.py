from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, CustomPasswordChangeForm,CustomUserChangeForm
from django.contrib import messages
from groupmeet import *
from account.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect("userCalendar_view")
        
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("userCalendar_view")
        else:
            messages.add_message(request, messages.ERROR, ' 가입하지 않은 계정이거나, 잘못된 비밀번호입니다')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request,"login.html", {"form":form})

def logout_view(request):
    logout(request)
    return redirect("login")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form':form})

@login_required
def mypage_view(request):
    if request.user.is_authenticated:
        userinfo=CustomUser.objects.get(nickname=request.user.nickname)
        return render(request,'mypage.html',{'userinfo':userinfo})
    else:
        return render(request,'forbidden.html')

def change_userinfo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, instance = request.user)
            if form.is_valid():
                form.save()
                messages.success(request, '회원정보가 수정되었습니다.')
                return redirect('mypage')
        else:
            form = CustomUserChangeForm(instance=request.user)
        return render(request, 'changeuserinfo.html', {'form':form})
    else:
        return render(request,'forbidden.html')

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
                return redirect('changepw')
            # else:
            #     messages.error(request, 'Please correct the error below.')
        else:
            form = CustomPasswordChangeForm(request.user)
        return render(request, 'changePassword.html', {'form': form})
    else:
        return render(request,'forbidden.html')