from django.db import models
from django.utils import timezone
# from django.conf import settings
# i need product for order and user who is requesting it
from product.models import ProductModel
# this is for our custom user model
from account.models import Customer


class OrderModel(models.Model):
    status_choices = (
        (1, 'Not Packed'), 
        (2, 'Ready for Shipment'), 
        (3, 'Shipped'), 
        (4, 'Delivered')
    )
    payment_status_choices = (
        (1, 'SUCCESS'), 
        (2, 'FAILURE'), 
        (3, 'PENDING'),
    )

    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_user")
    order_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    
    status = models.IntegerField(choices=status_choices, default=1)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.IntegerField(choices=payment_status_choices, default=3)
    transactionId = models.CharField(max_length=150, default=0) 
    # RELATED TO RAZORPAY INFORMATION   
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    # User Information and Address
    full_name = models.CharField(max_length=110, default='')
    address = models.CharField(max_length=250, default = '')
    city = models.CharField(max_length=100, default='')
    # phone_number = models.CharField(max_length=20)
    # post_code = models.CharField(max_length=10)
    # billing_status = models.BooleanField(default=False)

    datetime_of_payment = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)



class OrderItem(models.Model):
    order = models.ForeignKey(OrderModel, related_name="items", on_delete=models.CASCADE)

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="order_items",)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)




# class Address(models.Model):
#     customer = models.ForeignKey(UserBase, on_delete=models.SET_NULL, null=True, blank=True)
#     country = models.CharField(max_length=70)
#     fullName = models.CharField(max_length=150)
#     mobileNumber = models.CharField(max_length=20)
#     pinCode = models.CharField(max_length=10)
#     houseNumber = models.CharField(max_length=50)
#     area = models.CharField(max_length=50)
#     landMark = models.CharField(max_length=100)
#     town = models.CharField(max_length=70)
#     state = models.CharField(max_length=50)
#     distict = models.CharField(max_length=40)

#     publish = models.DateTimeField(default=timezone.now)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.fullName

