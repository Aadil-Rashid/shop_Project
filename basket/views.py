from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required

from .basket import BaseBasket
from product.models import ProductModel


# @login_required
def basketSummaryView(request):
    basket = BaseBasket(request)
    
    context = {"basket": basket,}
    return render(request, 'basket/basketSummary.html', context)


def basketAddView(request):
    basket = BaseBasket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_Qty = int(request.POST.get('productQty'))
        
        product = get_object_or_404(ProductModel, id=product_id)
        
        basket.add(product=product, product_Qty=product_Qty)
        basketqty = basket.__len__()

        # Jsone response is send to the frontend after succssful ajax request has met
        response = JsonResponse({'qty': basketqty})

        return response


def basketdeleteView(request):
    basket = BaseBasket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))        
        basket.delete(product=product_id)
        basketqty = basket.__len__()
        basketTotal = basket.get_total_price()

        # Jsone response is send to the frontend after succssful ajax request has met
        response = JsonResponse({'qty': basketqty, 'subTotal': basketTotal })

        return response


def basketUpdateView(request):
    basket = BaseBasket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))        
        product_qty = int(request.POST.get('productqty'))   

        basket.update(product=product_id, qty=product_qty)

        basketQty = basket.__len__()
        basketTotal = basket.get_total_price()

        # Jsone response is send to the frontend after succssful ajax request has met
        response = JsonResponse({'qty': basketQty, 'subTotal': basketTotal })

        return response
