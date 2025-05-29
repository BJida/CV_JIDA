from django.core.mail import send_mail
from django.shortcuts import render
from .models import Order

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order, created = Order.objects.get_or_create(user=request.user, paid=False)
    item, created = OrderItem.objects.get_or_create(order=order, product=product)
    item.quantity += 1
    item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    order = Order.objects.get(user=request.user, paid=False)
    item = OrderItem.objects.get(order=order, product_id=product_id)
    item.delete()
    return redirect('cart')

@login_required
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, paid=False)
    return render(request, 'store/cart.html', {'order': order})

@login_required
def checkout(request):
    order = Order.objects.get(user=request.user, paid=False)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(item.product.price * 100),
                'product_data': {
                    'name': item.product.name,
                },
            },
            'quantity': item.quantity,
        } for item in order.items.all()],
        mode='payment',
        success_url=request.build_absolute_uri('/store/payment-success/'),
        cancel_url=request.build_absolute_uri('/store/cart/'),
    )
    return redirect(session.url, code=303)

# @login_required
# def payment_success(request):
#     order = Order.objects.get(user=request.user, paid=False)
#     order.paid = True
#     order.save()
#     return render(request, 'store/payment_success.html')

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def signin(request):
    if request.method == "POST":
        username = request.POST.get("id_username")
        password = request.POST.get("id_password")
        print(username,"******", password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect("index")  # Redirige vers la page d'accueil ou autre
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "registration/login.html")

@login_required
def payment_success(request):
    order = Order.objects.get(user=request.user, paid=False)
    order.paid = True
    order.save()

    send_mail(
        'Commande confirmée',
        f'Merci pour votre commande #{order.id}. Total: {order.total_price()} €',
        'boutique@example.com',
        [request.user.email],
    )

    return render(request, 'store/payment_success.html')
