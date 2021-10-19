from product.models import ProductModel
from django.conf import settings
from decimal import Decimal


class BaseBasket():
    """
    A Base Basket class, providing some default behaviours that are can
    be inherited or overrided as necessary.
    """

    def __init__(self, request):
        self.session = request.session

        basket = self.session.get('skey')   #skey == sessionKey
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}

        self.basket = basket


    def add(self, product, product_Qty):
        """
        Adding and updating the users basket session data.
        """
        product_id = str(product.id)
       

        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_Qty
            
        else:  #if product is not in basket then we will add price and qty of that prod in our basket
            self.basket[product_id] = {'price': str(product.price), 'qty': product_Qty}

        self.save()


    # Making class iterable
    def __iter__(self):
        """
        Collect the product_id in the session data to query the database and return products
        """
        product_ids = self.basket.keys()
        # print('Product_ids: ', product_ids)    --->  Product_ids:  dict_keys(['2', '1'])
        # print(type(product_ids))    --->         <class 'dict_keys'>

        products = ProductModel.products.filter(id__in=product_ids)
        basket = self.basket.copy()
        
        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item


    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())


    # new function for calculating subTotal
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    # def get_subtotal_price(self):
    #     return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    # def get_total_price(self):

    #     subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    #     if subtotal == 0:
    #         shipping = Decimal(0.00)
    #     else:
    #         shipping = Decimal(11.50)

    #     total = subtotal + Decimal(shipping)
    #     return total

    # delete funtionality of our session
    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
        self.save()


    # Update funtionality of our session
    def update(self, product, qty):
        """
        Update Values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty

        self.save()

    def clear(self):
        # Remove basket from session
        del self.session['skey']
        self.save()

    # Save funtion for saving things after changing in session
    def save(self):
        self.session.modified = True
        
