# -*- coding: utf-8 -*-
from django import forms
from attestation.models import *
from django.utils.translation import ugettext_lazy as _, ugettext


class RequestForm(forms.Form):
    first_name = forms.CharField(max_length=32, label=_('First name'), required=True)
    last_name = forms.CharField(max_length=32, label=_('Last name'))
    middle_name = forms.CharField(max_length=32, label=_('Middle name'))
    genitive = forms.CharField(max_length=96, label=_('Genitive'))
    birth_date = forms.DateField(label=_('Birth date'))
    post_date = forms.DateField(label=_('Appointment date'))
    email = forms.EmailField(required=True, label=_('E-Mail'))
    official_email = forms.EmailField(required=True, label=u'E-Mail организации')
    phone = forms.CharField(required=False, label=_('Phone'), max_length=12)
    post = forms.ModelChoiceField(queryset=Post.objects.all(), label=_('Post'))
    discipline = forms.CharField(required=False, label=_('Discipline'), max_length=64)

    # Must be
    territory = forms.ModelChoiceField(queryset=Territory.objects.all(), label=_('Territory'), required=False)
    # or
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), label=_('Child organization'),
                                          required=False)

    organization_name = forms.CharField(max_length=512, label=_('Organization name'), required=False,
                                        widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}))

    organization_type = forms.ChoiceField(choices=OTYPES, label=u'Направление деятельности', required=True)

    with_qualification = forms.ModelChoiceField(queryset=Qualification.objects.exclude(for_confirmation=True),
                                                label=_('With qualification'), required=False, empty_label='не имею')
    expiration_date = forms.DateField(label=_('Expiration date'), required=False)
    organization_experience = forms.IntegerField(label=_('Experience in organization'))
    post_experience = forms.IntegerField(label=_('Experience in post'))

    # first education
    edu_institution = forms.CharField(max_length=512, label=_('Educational institution'),
                                      widget=forms.Textarea(attrs={"rows": 3, "cols": 80}))
    edu_speciality = forms.CharField(max_length=128, label=_('Speciality'))
    edu_qualification = forms.CharField(max_length=128, label=_('Qualification'))
    edu_diploma_year = forms.IntegerField(label=_('Diploma year'))

    # second education
    edu_institution2 = forms.CharField(max_length=512, label=_('Educational institution'), required=False,
                                       widget=forms.Textarea(attrs={"rows": 3, "cols": 80}))
    edu_speciality2 = forms.CharField(max_length=128, label=_('Speciality'), required=False)
    edu_qualification2 = forms.CharField(max_length=128, label=_('Qualification'), required=False)
    edu_diploma_year2 = forms.IntegerField(label=_('Diploma year'),
                                           required=False)

    # additional info
    degrees = forms.ModelMultipleChoiceField(queryset=Degree.objects.all(), label=_('Degree'),
                                             required=False)
    academic_title = forms.ModelChoiceField(queryset=AcademicTitle.objects.all(), label=_('Academic title'),
                                            required=False)

    achievements = forms.ModelMultipleChoiceField(queryset=Achievement.objects.all(),
                                                  label=_('Achievements and titles'), required=False)

    qualification = forms.ModelChoiceField(queryset=Qualification.objects.filter(is_active=True),
                                           label=_('Qualification category'))
    presence = forms.BooleanField(label=_('Presence'), required=False)
    experience = forms.IntegerField(label=_('Experience'))
    ped_experience = forms.IntegerField(label=_('Pedagogical experience'))
    trainings = forms.CharField(label=_('Trainings'), required=False,
                                max_length=512, widget=forms.Textarea(attrs={"rows": 5, "cols": 80}))
    results = forms.CharField(widget=forms.Textarea(attrs={"rows": 8, "cols": 80, 'maxlength': 1200}),
                              label=_('Results'))
    simple_doc = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "cols": 80, 'maxlength': 256}),
                                 label=u'Документ', required=False)

    identity = forms.BooleanField(required=True, label=u'Даю согласие на обработку моих персональных данных')

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('identity'):
            raise forms.ValidationError(u'Необходимо подтвердить согласие на обработку персональных данных!')
        if cleaned_data.get('with_qualification') and not cleaned_data.get('expiration_date'):
            self._errors['expiration_date'] = ugettext('Field required.')
            raise forms.ValidationError(_('You must define expiration date if you have qualification'))

        if cleaned_data.get('territory') and not cleaned_data.get('organization_name'):
            self._errors['organization_name'] = ugettext('Field required.')
            raise forms.ValidationError(_('Fields Territory and Organization name both must be filled.'))

        if not cleaned_data.get('territory') and not cleaned_data.get('organization'):
            self._errors['territory'] = ugettext('Field required.')
            self._errors['organization_name'] = ugettext('Field required.')
            self._errors['organization'] = ugettext('Field required.')
            raise forms.ValidationError(
                _('You must fill Territory and Organization name fields or Organization fields'))

        if cleaned_data.get('edu_institution2'):
            if not (cleaned_data.get('edu_speciality2') and cleaned_data.get('edu_qualification2')
                    and cleaned_data.get('edu_diploma_year2')):
                self._errors['edu_speciality2'] = ugettext('Field required.')
                self._errors['edu_diploma_year2'] = ugettext('Field required.')
                self._errors['edu_qualification2'] = ugettext('Field required.')
                raise forms.ValidationError(_('If you have second education, you must fill all fields'
                                              ' for second education'))
        else:
            cleaned_data['edu_institution2'] = None
            cleaned_data['edu_speciality2'] = None
            cleaned_data['edu_diploma_year2'] = None
            cleaned_data['edu_qualification2'] = None

        return cleaned_data