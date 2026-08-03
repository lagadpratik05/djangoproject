from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination


class Booking(models.Model):
    STATUS_CHOICES = (
    ("pending", "Pending"),
    ("paid", "Paid"),
    ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    persons = models.PositiveIntegerField()
    mobile_number = models.CharField(max_length=15)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_screenshot = models.ImageField(upload_to="payments/", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.destination.name} - {self.user.email}"


    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)

from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    rating = models.IntegerField()  # 1–5
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"