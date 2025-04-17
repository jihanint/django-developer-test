from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_module/product_list.html', {'products': products})

@login_required
@permission_required('product_module.add_product', raise_exception=True)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Successfully added product: {product.name}')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_module/product_form.html', {'form': form})

@login_required
@permission_required('product_module.change_product', raise_exception=True)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Successfully updated product: {product.name}')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_module/product_form.html', {'form': form})

@login_required
@permission_required('product_module.delete_product', raise_exception=True)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, f'Successfully deleted product: {product.name}')
        return redirect('product_list')

    return render(request, 'product_module/product_confirm_delete.html', {'product': product})
