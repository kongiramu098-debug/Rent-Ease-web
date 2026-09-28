from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Product, Booking, Shop

def home(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects.filter(shop__approved=True)
    if q: products = products.filter(Q(name__icontains=q)|Q(category__icontains=q)|Q(brand__icontains=q)|Q(shop__city__icontains=q))
    return render(request, "home.html", {"products": products, "q": q})

def register(request):
    if request.method == "POST":
        username=request.POST.get("username","").strip()
        email=request.POST.get("email","").strip()
        password=request.POST.get("password","")
        if not username or not email or len(password)<8:
            messages.error(request,"Enter a username, email, and password of at least 8 characters.")
        elif User.objects.filter(username=username).exists():
            messages.error(request,"That username is already taken.")
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            login(request,user)
            return redirect("home")
    return render(request,"auth.html",{"register":True})

def login_view(request):
    if request.method=="POST":
        user=authenticate(request,username=request.POST.get("username",""),password=request.POST.get("password",""))
        if user:
            login(request,user); return redirect("home")
        messages.error(request,"Invalid username or password.")
    return render(request,"auth.html",{"register":False})

def logout_view(request):
    logout(request); return redirect("home")

@require_POST
def book(request, product_id):
    if not request.user.is_authenticated: return redirect("login")
    product=get_object_or_404(Product,pk=product_id,shop__approved=True)
    try:
        start=date.fromisoformat(request.POST.get("start_date",""))
        end=date.fromisoformat(request.POST.get("end_date",""))
    except ValueError:
        messages.error(request,"Please choose valid rental dates."); return redirect("home")
    if start < date.today() or end < start:
        messages.error(request,"Choose a start date from today and an end date on or after it."); return redirect("home")
    days=(end-start).days+1
    with transaction.atomic():
        overlapping=Booking.objects.select_for_update().filter(product=product,start_date__lte=end,end_date__gte=start).exclude(status__in=["Cancelled","Completed","Returned"]).count()
        if overlapping >= product.quantity:
            messages.error(request,"Sorry, this product is already booked for those dates.")
        else:
            Booking.objects.create(customer=request.user,product=product,start_date=start,end_date=end,rental_days=days,total_amount=product.daily_price*days)
            messages.success(request,"Booking request created. Payment is not enabled in this prototype.")
    return redirect("my_bookings")

def my_bookings(request):
    if not request.user.is_authenticated: return redirect("login")
    return render(request,"bookings.html",{"bookings":Booking.objects.filter(customer=request.user).select_related("product","product__shop").order_by("-created_at")})

@require_POST
def update_status(request, booking_id):
    if not request.user.is_staff: return HttpResponseForbidden("Admin access required for demo status updates.")
    booking=get_object_or_404(Booking,pk=booking_id)
    status=request.POST.get("status")
    if status in dict(Booking.STATUS): booking.status=status; booking.save(update_fields=["status"])
    return redirect("my_bookings")

def assistant(request):
    answer=""
    if request.method=="POST":
        query=request.POST.get("query","").strip()
        import re
        budget_match=re.search(r"(?:under|below|less than)\s*₹?\s*(\d+)",query.lower())
        budget=Decimal(budget_match.group(1)) if budget_match else None
        products=Product.objects.filter(shop__approved=True)
        for word in ["laptop","smartphone","phone","camera","tablet","projector","speaker"]:
            if word in query.lower():
                category={"phone":"Smartphones","smartphone":"Smartphones"}.get(word,word.title()+"s" if word not in ["laptop","camera","tablet","projector","speaker"] else {"laptop":"Laptops","camera":"Cameras","tablet":"Tablets","projector":"Projectors","speaker":"Speakers"}[word])
                products=products.filter(category__iexact=category); break
        if budget: products=products.filter(daily_price__lte=budget)
        matches=list(products[:5])
        answer="Here are matching listings from the database:" if matches else "I couldn't find a matching listing. Try a different category or budget."
        return render(request,"assistant.html",{"answer":answer,"matches":matches,"query":query})
    return render(request,"assistant.html")
