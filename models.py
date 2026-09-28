from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100, default="Tirupati")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    approved = models.BooleanField(default=True)
    def __str__(self): return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [(x, x) for x in ["Laptops","Smartphones","Cameras","Tablets","Projectors","Speakers","Gaming consoles","Accessories"]]
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=140)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    daily_price = models.DecimalField(max_digits=9, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
    image_url = models.URLField(blank=True)
    def __str__(self): return self.name

class Booking(models.Model):
    STATUS = [(s,s) for s in ["Booking Pending","Booking Confirmed","Payment Completed","Ready for Pickup","Out for Delivery","Rental Active","Return Requested","Returned","Completed","Cancelled"]]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rental_bookings")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    rental_days = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS, default="Booking Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"#{self.pk} {self.product.name}"
