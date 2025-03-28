from django.db import models
from django.contrib.auth.models import User

class Art(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='art/')
    description = models.TextField()
    start_price = models.FloatField()
    fixed_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Bid(models.Model):
    art = models.ForeignKey(Art, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid ${self.amount} on {self.art.name}"
