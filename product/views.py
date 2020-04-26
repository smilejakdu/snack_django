import jwt, bcrypt, json
from  django.db        import IntegrityError
from  django.db.models import Count, Q , Sum
from  django.views     import View
from  django.http      import HttpResponse, JsonResponse
from .models           import Category , Product , CategoryProduct


class CategoryView(View):
    def get(self , request):
        data = Category.objects.values()
        return JsonResponse({"data" : list(data)} , status=200)


class ProductView(View):
    def get (self , request , category_name):

        try :
            sort_by = request.GET.get('sort_by' , 'id')
            offset  = int(request.GET.get('offset' , 0))
            limit   = int(request.GET.get('limit' , 50))

            product_info = (Product.
                            objects.
                            filter(category__name = category_name).
                            order_by(sort_by).
                            values('id',
                                   'name',
                                   'image',
                                   'retail_price',
                                  )[offset:offset+limit])

            return JsonResponse({"data":list(product_info)},status=200)

        except ValueError:
            return JsonResponse({"ERROR":"VALUDE_ERROR"} , status=400)

        except TypeError:
            return JsonResponse({"ERROR":"INVALID_TYPE"} , status=400)

class ProductDetailView(View):
    def get(self , request , product_id):

        try:
            data = (Product.
                    object.
                    filter(id = product_id).
                    values())

            return JsonResponse({"data" : list(data)} , status=200)

        except TypeError:
            return JsonResponse({"ERROR" : "INVALID_TYPE"} , status=400)

        except Exception as e :
            return JsonResponse({"ERROR" : e} , status=400)


class SearchView(View):
    def get(self , request):
        query = request.GET.get('keyword' , None)

        if len(query) > 0:
            search_data = (Product.
                           objects.
                           filter(Q(name__icontains=query)).
                           values('id' ,
                                  'name' ,
                                  'image',
                                  'retail_price',
                                  'price'))

            return HttpResponse(status=200)

        return JsonResponse({"error" : "invalid keyword"} , status=400)
