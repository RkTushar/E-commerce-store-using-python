from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Order   # ✅ Import Order model

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

# ✅ Checkout View
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        total_price = 0
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            quantity = cart[str(product.id)]
            total_price += product.price * quantity

        # ✅ Save Order in database
        order = Order.objects.create(
            name=name,
            address=address,
            email=email,
            phone=phone,
            total_price=total_price
        )

        # ✅ Clear cart after successful order
        request.session['cart'] = {}
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('home')

    total_price = 0
    products = Product.objects.filter(id__in=cart.keys())
    for product in products:
        quantity = cart[str(product.id)]
        total_price += product.price * quantity

    return render(request, 'store/checkout.html', {'total_price': total_price})
