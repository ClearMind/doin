from config.models import MenuItem
from datetime import date
import settings

def menu(request):
    return {"menu_items": MenuItem.objects.all()}

def base_context(request):
    return {
        "company": settings.company,
        "app_name": settings.app_name,
        "date": date.today()
    }
