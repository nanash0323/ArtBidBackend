from django.db import models
from django.contrib.auth.models import User
import uuid  

class Art(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="arts")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='art_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Bid(models.Model):
    art = models.ForeignKey(Art, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid ${self.amount} on {self.art.name}"
