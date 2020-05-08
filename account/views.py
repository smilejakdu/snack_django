import jwt, bcrypt, json , re , requests

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from  django.db             import IntegrityError
from  django.db.models      import Count, Q , Sum
from  django.views          import View
from  django.http           import HttpResponse, JsonResponse

from .utils                 import login_check
from .models                import Account

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
                password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
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

                if bcrypt.checkpw(data['password'].encode() ,
                                  account.password.encode('utf-8')):

                    token = jwt.encode({"user":account.id},
                                       SECRET_KEY['secret'],
                                       algorithm = ALGORITHM)

                    return JsonResponse({"token" : token.decode('utf-8')} , status=200)

                return HttpResponse(status=400)

            return HttpResponse(status=401)

        except KeyError:
            return JsonResponse({"ERROR":"INVALID_KEYS"} , status=400)

        except Exception as e :
            return JsonResponse({'error' : e} , status=400)


class ProfileView(View):
    @login_check
    def get(self , request):
        account_data = (Account.
                        objects.
                        filter(user_id = request.
                                       account.
                                       user_id).values())

        return JsonResponse({'data':list(account_data)},status=200)

    @login_check
    def post(self , request):
        data     = json.loads(request.body)
        account  = Account.objects.get(user_id = request.account.user_id)

        try :
            if Account.objects.filter(user_id = account.user_id):
                if bcrypt.checkpw(data['password'].encode('utf-8') ,
                                  account.password.encode('utf-8')):

                    account.update(
                        user_id = data['user_id'],
                        name    = data['name'],
                        email   = data['email'],
                        gender  = data['gender'],
                        birth   = data['birth'],
                        post    = data['post'],
                    )

                    return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'error':'invalid_key'},status=400)

        except ValueError:
            return HttpResponse(status=400)

        except Exception as e:
            return JsonResponse({'error':e} , status=400)

class KakaoView(View):
    def post(self , request):
        access_token = request.headers.get('Authorization' , None)

        if access_token is None:
            return HttpResponse(status=400)

        try :
            url     = 'https://kapi.kakao.com/v2/user/me'
            headers = {
                "Host"          : "kapi.kakao.com",
                "Authorization" : f"Bearer {access_token}",
                "Content-type"  : "application/x-www-from-urlencoded;charset=utf-8"
            }
            req           = requests.get(url , headers =headers)
            req_json      = req.json()

            kakao_id      = req_json.get('id'            , None)
            kakao_account = req_json.get('kakao_account' , None)
            kakao_email   = kakao_account.get('email'    , None)

            if Account.objects.filter(email=kakao_email).exists():

                token = jwt.encode({'email' : kakao_email},
                                   SECRET_KEY['secret'],
                                   algorithm=ALGORITHM).decode("utf-8")

                return JsonResponse({"token" : token} , status = 200)

            Account(
                email    = kakao_email ,
                kakao_id = kakao_id,
            ).save()

        except KeyError:
            return JsonResponse({'error':'invalid_key'} , status=400)

        except jwt.DecodeError:
            return HttpResponse(status=400)

        except Exception as e:
            return JsonResponse({'error' : e} , status=400)

