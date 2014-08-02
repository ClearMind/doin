# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.translation import ugettext_lazy as _
from config.models import NewsItem

def index(request):
    """
    Index page view
    """
    title = _('Home page')

    news = NewsItem.objects.all()

    c = RequestContext(request, locals())
    template = loader.get_template("base.html")

    return HttpResponse(template.render(c))