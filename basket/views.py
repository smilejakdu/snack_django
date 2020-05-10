import jwt, bcrypt, json

from  django.db.models import Count, Q , Sum
from  django.views     import View
from  django.http      import HttpResponse, JsonResponse

from .models           import Basket
from account.utils     import login_check

class BasketView(View):
    @login_check
    def post(self , request):
        return

    @login_check
    def get(self , request , user_id , product_id):
        return

class BaseketDetailView(View):
    @login_check
    def post(self, request , user_id , product_id):
        return

    @login_check
    def delete(self , request , user_id , product_id):
        return
