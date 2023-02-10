from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# Create your models here.

class Cart(models.Model):
    cart_id     =   models.CharField(max_length=250, blank=True)
    date_added  =   models.DateField(auto_now_add=True)

    def __str__(self):
        if self.cart_id is not None:
            return self.cart_id
        else:
            return ''


class CartItem(models.Model):
    user        =   models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product     =   models.ForeignKey(Product, on_delete=models.CASCADE)
    variations  =   models.ManyToManyField(Variation, blank=True)
    cart        =   models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity    =   models.IntegerField()
    is_active   =   models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        if self.product is not None:
            return self.product
        else:
            return ''
