from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Module
from django.urls import reverse
from django.db import connection
import os
from django.core.management import call_command
from django.contrib.auth import logout

MODULES = {
    "product_module": {
        "name": "Product Management",
        "version": "1.0",
        "url": "/product/",
        "install_query": """
            CREATE TABLE IF NOT EXISTS "product_module_product" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "name" varchar(255) NOT NULL,
                "barcode" varchar(50) NOT NULL UNIQUE,
                "price" decimal NOT NULL,
                "stock" integer unsigned NOT NULL CHECK ("stock" >= 0)
            )
        """,
        "delete_query": """
            DROP TABLE IF EXISTS "product_module_product"
        """
    }
}

def upgrade_module(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
        call_command("makemigrations", module.name)
        call_command("migrate", module.name)
        module.upgrade(MODULES[module.name]["version"])
        messages.success(request, "Module upgraded successfully!")
    except Exception as e:
        messages.error(request, f"Upgrade failed: {e}")
    return redirect(reverse('module_list'))

def module_list(request):
    # Ensure the product_module is in the database
    for module_name, module_info in MODULES.items():
        Module.objects.get_or_create(
            name=module_name,
            defaults={
                "installed": False,
                "version": module_info["version"],
                "installation_status": "Not Installed",
                "install_query": module_info["install_query"],
                "delete_query": module_info["delete_query"]
            }
        )
    modules = Module.objects.all()
    return render(request, 'engine/module_list.html', {'modules': modules, 'available_modules': MODULES})

def install_module(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
        module.installed = True
        module.installation_status = "Installing..."
        module.save()
        with connection.cursor() as cursor:
            cursor.execute(module.install_query)
        module.installation_status = "Installed"
        module.save()
        messages.success(request, f"{module.name} installed successfully.")
        return redirect(MODULES[module.name]["url"])
    except Module.DoesNotExist:
        messages.error(request, "Module does not exist.")
    return redirect(reverse('module_list'))

def uninstall_module(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
        with connection.cursor() as cursor:
            cursor.execute(module.delete_query)
        module.installed = False
        module.installation_status = "Not Installed"
        module.save()
        messages.success(request, f"{module.name} uninstalled successfully.")
    except Module.DoesNotExist:
        messages.error(request, "Module does not exist.")
    return redirect(reverse('module_list'))

def custom_logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')
