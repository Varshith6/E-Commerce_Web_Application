from .models import CATEGORY_CHOICES

def basecategories(request):
    return {'categories': CATEGORY_CHOICES}