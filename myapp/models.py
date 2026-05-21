from django.db import models
from django.contrib.auth.models import User


SCRAP_TYPES = [
    ('metal', 'Metal / Iron'),
    ('paper', 'Paper / Cardboard'),
    ('electronics', 'Electronics (E-waste)'),
    ('plastic', 'Plastic'),
    ('battery', 'Battery'),
    ('silver', 'Silver'),
    ('brass','Brass'),
    ('copper','Copper'),
    ('other', 'Other'),
]

class ScrapPrice(models.Model):
    material = models.CharField(max_length=100)
    scrap_type = models.CharField(max_length=20, choices=SCRAP_TYPES)
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20, default='PKR/kg')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.material} — {self.price_per_kg} {self.unit}"

class QuoteRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    scrap_type = models.CharField(max_length=20, choices=SCRAP_TYPES, unique=True)
    weight_kg = models.FloatField()
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.scrap_type} {self.weight_kg}kg"

class PickupBooking(models.Model):
    STATUS = [('pending','Pending'),('confirmed','Confirmed'),('done','Done')]
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    scrap_type = models.CharField(max_length=20, choices=SCRAP_TYPES)
    pickup_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.pickup_date}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.created_at.date()}"


class Comment(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:40]}"
    
#page views trackers
class PageView(models.Model):
    path       = models.CharField(max_length=200)   # which page
    ip_address = models.GenericIPAddressField()
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.path} — {self.ip_address} — {self.visited_at.date()}"