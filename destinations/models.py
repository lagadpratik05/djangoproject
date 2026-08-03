from django.db import models

class Destination(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
    )

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
        # Images (simple version for now)
    image = models.ImageField(upload_to="destinations/", blank=True, null=True)
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

        # Dates
    start_date = models.DateField()
    end_date = models.DateField()

    best_season_start = models.DateField(null=True, blank=True)
    best_season_end = models.DateField(null=True, blank=True)

    capacity_per_day = models.IntegerField(default=20)

    transport_mode = models.CharField(max_length=100, blank=True)

    rating = models.FloatField(default=0)


    whatsapp_group_link = models.URLField(blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
