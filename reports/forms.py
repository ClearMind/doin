from django import forms
from django.utils.translation import ugettext_lazy as _


class DatePeriodForm(forms.Form):
    fromdate = forms.DateField(required=True, label=_('From date'), input_formats=['%d.%m.%Y'])
    todate = forms.DateField(required=True, label=_('To date'), input_formats=['%d.%m.%Y'])


class QuarterForm(forms.Form):
    quarter = forms.ChoiceField(label=u'', required=True, choices=[(x, x) for x in ('I', 'II', 'III', 'IV')])
    year = forms.IntegerField(label=u'', required=True, min_value=2014, max_value=2050)
