import json
from .models import Review

from product.models import Product
from account.models import Account

from django.views  import View
from django.http   import HttpResponse , JsonResponse
from account.utils import login_check

class ReviewView(View):

    @login_check
    def post(self , request , product_id):
        data    = json.load(request.body)
        title   = data.get("title",   None)
        content = data.get("content", None)

        try:

            if Account.objects.filter(id = request.account.id).exist():
                if title and content:
                    Review(
                        title   = title,
                        content = content ,
                        files   = data['files'],
                    ).save()

                    return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status=400)

        except Exception as e:
            return JsonResponse({"message" : e} , status=400)

    def get(self , request , product_id):
        sort_by = request.GET.get('sort_by' , 'id')
        offset  = int(request.GET.get('offset' , 0))
        limit   = int(request.GET.get('limit' , 20))

        review_data = (Review.
                       objects.
                       filter(product_id = product_id).
                       order_by(sort_by).
                       values()[offset:offset+limit])

        return JsonResponse({"message" : list(review_data)} , status=200)

class ReviewDetailView(View):

    @login_check
    def post(self , request , product_id , review_id):
        data    = json.load(request.body)
        title   = data.get('title' , None)
        content = data.get('content', None)

        try :
            review_data =  Review.objects.get(id         = review_id ,
                                              product_id = product_id ,
                                              user_id    = request.account.id)

            if title and content:
                review_data.title   = title
                review_data.content = content
                review_data.save()

                return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"} , status=400)

        except Exception as e :
            return JsonResponse({"message":e} , status=400)

    @login_check
    def delete(self , request , product_id , review_id):

        try:
            review_data =  Review.object.get(id         = review_id ,
                                             product_id = product_id ,
                                             user_id    = request.account.id)

            review_data.delete()

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"} , status=400)

        except Exception as e:
            return JsonResponse({"message" : e}, status=400)

