# filepath: /C:/Users/rifqi alfurqan/Pictures/modular_project/modular_project/views.py
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def custom_logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')