from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from finance_tracker.models import CustomUser


def register_view(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        first_name = request.POST.get("f_name", None)
        last_name = request.POST.get("l_name", None)
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        password1 = request.POST.get("confirm_password", None)
        if not username or not email or not password or not password1:
            return HttpResponse("All feilds are required!")
        if password != password1:
            return HttpResponse("Passwords don't match!")
        user = CustomUser.objects.filter(username=username).first()
        if user:
            return HttpResponse(f'User with username "{username}" already exists')
        user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        return redirect("login")
    

def login_view(request):
    if request.merthod == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        if not username or not password:
            return HttpResponse("Fields are required")
        user = CustomUser.objects.filter(username=username).first()
        if not user:
            return HttpResponse("User not found")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            redirect(request, "get_transaction")
        return HttpResponse("User not found")

def logout_view(request):
    logout(request)
    return redirect('login')



def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        if not username or not password:
            return HttpResponse("Username or password are required")
        user = CustomUser.objects.filter(username=username).first()
        if not user:
            return HttpResponse("User not found")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("get_transaction")
        return HttpResponse("User not found")
    
def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        if not username or not password:
            return HttpResponse("Username and password are required!")
        user = CustomUser.objects.filter(username=username).first()
        if not user:
            return HttpResponse("User not found")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("get_transaction")
        return HttpResponse("User not found")
        
def logout_view(request):
    logout(request)
    return redirect("login")


