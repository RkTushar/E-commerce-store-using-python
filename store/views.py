from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

# ✅ Home page view (listing all products)
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# ✅ Single product detail view
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# ✅ Add to Cart view
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

# ✅ View Cart
def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        total = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })
        total_price += total

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# ✅ Remove from Cart
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
    return redirect('view_cart')
