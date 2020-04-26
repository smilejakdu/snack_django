import jwt, bcrypt, json , re
from  django.db             import IntegrityError
from  django.db.models      import Count, Q , Sum
from  django.views          import View
from  django.http           import HttpResponse, JsonResponse
from .models                import Account
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from snack_mart.my_settings import (SECRET_KEY,
                                    ALGORITHM,
                                    )

class SignUpView(View):

    def invalid_phone(self, phone):
        if re.match(r"^\d{3}?\d{4}?\d{4}$", phone):
            return False
        return True

    def post(self , request):
        data    = json.loads(request.body)
        email   = data.get('email' , None)
        user_id = data.get('user_id', None)

        try :
            validate_email(data['email'])
            if Account.objects.filter(user_id =user_id).exists():
                return JsonResponse({'ERROR':'DUPLICATED_ID'},status=400)

            if Account.objects.filter(email= email).exists():
                return JsonResponse({'ERROR' :'DUPLICATED_EMAIL'} , status=400)

            if self.invalid_phone(data['phone']):
                return HttpResponse(status=400)

            if len(data['password']) < 6:
                return JsonResponse({"error" :"password_short"},status=400)

            Account(
                name     = data['name'],
                user_id  = data['user_id'],
                password   = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                email    = data['email'],
                phone    = data['phone'],
            ).save()

            return HttpResponse(status=200)

        except KeyError:
            return HttpResponse(status=400)

        except ValidationError:
            return HttpResponse(status=400)

        except Exception as e :
            return JsonResponse({'error' : e} , status=400)

class SignInView(View):
    def post(self , request):
        data = json.loads(request.body)

        try :
            if Account.objects.filter(user_id =data['user_id']).exists():
                account = Account.objects.get(user_id = data['user_id'])

                if bcrypt.checkpw(data['password'].encode() , account.password.encode('utf-8')):
                    token = jwt.encode({"user":account.id} ,SECRET_KEY['secret'] , algorithm = ALGORITHM)

                    return JsonResponse({"token" : token.decode('utf-8')} , status=200)

                return HttpResponse(status=400)

            return HttpResponse(status=401)

        except KeyError:
            return JsonResponse({"ERROR":"INVALID_KEYS"} , status=400)

        except Exception as e :
            return JsonResponse({'error' : e} , status=400)


class ProfileView(View):
    def post(self , request):
        data     = json.loads(request.body)
        password = data.get('password' , None)
        try :
            if password :
                print(password)

            return JsonResponse({'data' : ''} , status=200)
        except TypeError:
            return JsonResponse({'error' : "invalid_type"},status=400)

        except Exception as e:
            return JsonResponse({'error' : e} , status=400)

class KakaoView(View):
    def post(self , request):
        return






