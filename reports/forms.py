from django import forms
from django.utils.translation import ugettext_lazy as _


class DatePeriodForm(forms.Form):
    fromdate = forms.DateField(required=True, label=_('From date'), input_formats=['%d.%m.%Y'])
    todate = forms.DateField(required=True, label=_('To date'), input_formats=['%d.%m.%Y'])
