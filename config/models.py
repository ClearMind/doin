from django.db import models
from django.utils.translation import ugettext_lazy as _


class MenuItem(models.Model):
    name = models.CharField(max_length=24, help_text=_("Menu item name"), verbose_name=_("name"))
    link = models.CharField(max_length=128, help_text=_("Local reference to application page"), verbose_name=_("link"))
    order = models.IntegerField(help_text=_("Order of item in menu"), verbose_name=_("order"))
    public = models.BooleanField(verbose_name=_('public'), help_text=_("Show for unauthorized users"), default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("menu item")
        verbose_name_plural = _("Menu items")
        ordering = ["order"]


class NewsItem(models.Model):
    title = models.CharField(verbose_name=_('news title'), max_length=256)
    text = models.TextField(verbose_name=_('news text'))
    date = models.DateField(verbose_name=_('publishing date'), auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('news item')
        verbose_name_plural = _('news items')
        ordering = ['-date', '-id']