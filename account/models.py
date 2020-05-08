from django.db import models

class Account(models.Model):
    name     = models.CharField(max_length=250, null = True)
    user_id  = models.CharField(max_length=250, unique = True)
    password = models.CharField(max_length=250)
    email    = models.CharField(max_length=250, unique = True)
    phone    = models.CharField(max_length=250, unique = True)
    coupon   = models.CharField(max_length=250, null = True)
    birth    = models.CharField(max_length=250)
    gender   = models.CharField(max_length=250)
    post     = models.CharField(max_length=250)
    kakao_id = models.IntegerField(max_length=250 , null=True)

    class Meta:
        db_table = 'accounts'
