from django.db      import models
from account.models import Account
from product.models import Product

# Create your models here.
class Basket(models.Model):
    user       = models.ForeignKey('account.Account',     on_delete=models.SET_NULL,  null=True)
    product    = models.ForeignKey('product.Product',     on_delete = models.CASCADE, null = True)
    quantity   = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'baskets'


