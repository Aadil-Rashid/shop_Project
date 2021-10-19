from .models import CategoryModel

# this will be available for all pages of my website and have added it in settings.py file also
def categories(request):
    return { 'categories': CategoryModel.objects.all()}
