from django.shortcuts import redirect
from django.contrib import messages
from engine.models import Module

class CheckInstallationStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path starts with /product/
        if request.path.startswith('/product/'):
            try:
                product_module = Module.objects.get(id=1)
                if product_module.installation_status != 'Installed':
                    messages.error(request, "Please install the product_module first.")
                    return redirect('/modules/modules/')
            except Module.DoesNotExist:
                messages.error(request, "Product module does not exist.")
                return redirect('/modules/modules/')
        response = self.get_response(request)
        return response