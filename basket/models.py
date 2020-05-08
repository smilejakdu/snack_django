from django.db      import models
from account.models import Account

# Create your models here.
class Basket(models.Model):
    user_id        = models.ForeignKey('Account', on_delete=models.SET_NULL , null=True)
    name           = models.CharField(max_length=250 , null=True)
    quantity       = models.CharField(max_length=250 , null=True)
    image          = models.CharField(max_length=300 , null=True)
    accumulate     = models.IntegerField(max_length=200 , null =True)
    price          = models.CharField(max_length=250 , null=True)
    delivery_price = models.CharField(max_length=250 , null = True)

    class Meta:
        db_table = 'baskets'


