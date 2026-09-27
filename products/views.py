from django.shortcuts import render,  redirect
from .models import Product, Order,  OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    products = Product.objects.all().order_by("-created_at")[:4]
    return render(request, "home.html", {
        "products": products
    })

def product(request):
    search = request.GET.get("search")
    category = request.GET.get("category")
    
    products = Product.objects.all()
    
    if search:
        products = products.filter(name__icontains=search)
        
    if category:
        products = products.filter(category=category)
        
    return render(request, "products.html", {"products": products})

    product = Product.objects.get(id=product_id)
def cart(request):
    if request.session.get("cart") and isinstance(request.session.get("cart"), list):
        request.session["cart"] = {}

    cart = request.session.get("cart", {})

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity =max(1,  int(request.POST.get("quantity", 1)))
        action = request.POST.get("action")

        if product_id:

            if action == "add":
                product = Product.objects.get(id=product_id)

                current_quantity = cart.get(product_id, 0)

                if current_quantity + quantity <= product.stock:
                    cart[product_id] = current_quantity + quantity
                else:
                    messages.error(request, "Product is out of stock.")
            
            elif action == "increase":
                if cart.get(product_id, 0) < product.stock:
                    cart[product_id] = cart.get(product_id, 0) + 1
                
            elif action == "decrease":
                if product_id in cart:
                    cart[product_id] -= 1

                    if cart[product_id] <= 0:
                        del cart[product_id]
                        
            elif action == "remove":
                if product_id in cart:
                    del cart[product_id]

            request.session["cart"] = cart
            request.session.modified = True
            
        return redirect("cart")

    cart_products = []

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        

        cart_products.append({
            "product": product,
            "quantity": quantity,
            "total": product.price * quantity,
        })
        


    grand_total = sum(item["total"] for item in cart_products)

    return render(request, "cart.html", {
        "cart_products": cart_products,
        "grand_total": grand_total,
    }) 
    
@login_required 
def checkout(request):
    cart = request.session.get("cart", {})

    # Cart empty hai to cart page par wapas
    if not cart:
        return redirect("cart")

    # Jab Place Order button submit ho
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        total = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)

            if quantity > product.stock:
                messages.error(
                    request,
                    f"Only {product.stock} items of {product.name} are available."
        )
                return redirect("cart")
        # Order create
        order = Order.objects.create(
            user=request.user,
            name=name,
            address=address,
            phone=phone
        )

        # Order ke products create karo
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
            product.stock -= quantity
            product.save()

            total += product.price * quantity

        # Order ka total save karo
        order.total = total
        order.save()

        # Cart empty karo
        request.session["cart"] = {}
        request.session.modified = True

        return redirect("order_success")

    # Checkout page ke liye order summary
    cart_products = []

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        cart_products.append({
            "product": product,
            "quantity": quantity,
            "total": product.price * quantity,
        })

    grand_total = sum(item["total"] for item in cart_products)

    return render(request, "checkout.html", {
        "cart_products": cart_products,
        "grand_total": grand_total,
    })
        
@login_required
        
            
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "orders.html", {
        "orders": orders
    })            
@login_required
def order_detail(request, id):
    order = Order.objects.get(id=id)

    return render(request, "order_detail.html", {
        "order": order
    })       

def order_success(request):
    return render(request, "order_success.html")


def product_detail(request, id):
    product = Product.objects.get(id=id)

    return render(request, "product_detail.html", {
        "product": product
    })
    
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("login")

    return render(request, "register.html")
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next", "home"))
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def cancel_order(request, id):
    order = Order.objects.get(id=id, user=request.user)

    if request.method == "POST" and order.status == "Pending":
        order.status = "Cancelled"
        order.save()

    return redirect("order_detail", id=order.id)