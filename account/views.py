import jwt, bcrypt, json
from  django.db             import IntegrityError
from  django.db.models      import Count, Q , Sum
from  django.views          import View
from  django.http           import HttpResponse, JsonResponse
from .models                import Account
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class SignUpView(View):
    def post(self , request):
        data    = json.loads(request.body)
        email   = data.get('email' , None)
        user_id = data.get('user_id', None)
        try :
            validate_email(data['email'])
            if Account.objects.filter(user_id = data['user_id']).exists():
                return JsonResponse({'error':'duplicated_email'},status=400)
        except :
            return HttpResponse(status=400)

class SignInView(View):
    def post(self , request):
        return

class KakaoView(View):
    def post(self , request):
        return






