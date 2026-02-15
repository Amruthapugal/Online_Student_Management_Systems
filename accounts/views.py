from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# ================= USER LOGIN =================
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect("students:dashboard")
        else:
            messages.error(request, "Invalid user credentials")

    return render(request, "login.html")


# ================= ADMIN LOGIN =================
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("students:admin_dashboard")
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, "admin_login.html")


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect("accounts:user_login")
