from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from myshop import settings

from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt

import razorpay
from order.models import OrderModel
from basket.basket import BaseBasket


razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))


@login_required
def paymentPageView(request):
    basket = BaseBasket(request)
    totalAmount = float(str(basket.get_total_price()))
    print('TotalAmount-------------------: ', totalAmount)
    if request.method == "POST":

        if totalAmount == 0:
            return HttpResponse("No product in Cart")

        order = OrderModel.objects.create(user = request.user)
        amount = int(totalAmount)
        order.total_amount=amount
        order.save()
        totalAmount = totalAmount

        callback_url = 'http://'+str(get_current_site(request))+"/payment/handlerequest/"
        
        dataPassToRazorPay = {
            'amount': totalAmount * 100,
            'currency': "INR",
            'receipt': order.order_id,
            'notes' : {'name':'Palav-Poshaak', 'Payment_For': 'Your_Product'}
        }
        # Here we are sending request to razorPay server(It return us an order Id)
        razorpay_order = razorpay_client.order.create(data=dataPassToRazorPay)
        order.razorpay_order_id = razorpay_order['id']

        order.save()


        context = { 'totalAmount':totalAmount, 'order_id': razorpay_order['id'], 'orderId':order.order_id,
                    'final_price': totalAmount, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url
        }
        return render(request, 'payment/paymentSummaryRazorpay.html', context)

    else:
        return HttpResponse('505 Page Not Found')


@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = OrderModel.objects.get(razorpay_order_id=order_id)
            except:
                return HttpResponse("505 File Not Found")

            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result == None:
                # amount = order_db.total_amount

                try:
                    # Here we need to capture the payment
                    # razorpay_client.payment.capture(payment_id, amount, {"currency":"INR"})
                    order_db.payment_status = 1
                    order_db.save()
                    return render(request, 'payment/paymentsuccess.html')

                except:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'payment/paymentfailed.html')
            elif result != None:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'payment/paymentfailed.html')
        except:
            return HttpResponse("505 not found")

