from .basket import BaseBasket


def basket(request):
    return {'basket': BaseBasket(request)}
