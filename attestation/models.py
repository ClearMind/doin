# coding=utf-8
import datetime
from hashlib import sha1

from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_save
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
import re

from settings import DEBUG, LANGUAGE_CODE

OTYPES = (
    ('common', u'общеобразовательное'),
    ('professional', u'профессиональное'),
    ('preschool', u'дошколное'),
    ('additional', u'дополнительное'),
    ('social', u'соц. защита'),
    ('cultural', u'культура'),
    ('correction', u'коррекционное'),
    ('sport', u'спортивное')
)


class Achievement(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('achievement')
        verbose_name_plural = _('achievements')
        ordering = ['name']


class SettlementType(models.Model):
    name = models.CharField(max_length=24, verbose_name=_('name'), unique=True)
    abbreviate = models.CharField(max_length=4, verbose_name=_('abbreviate'), unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('settlement type')
        verbose_name_plural = _('settlement types')
        ordering = ['name']


class Settlement(models.Model):
    type = models.ForeignKey(SettlementType, verbose_name=_('type'))
    name = models.CharField(max_length=20, verbose_name=_('name'), unique=True)

    def __unicode__(self):
        return "%s %s" % (self.type.abbreviate, self.name)

    class Meta:
        verbose_name = _('settlement')
        verbose_name_plural = _('settlements')
        ordering = ['name']


class Territory(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'), unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('territory')
        verbose_name_plural = _('territories')
        ordering = ['name']


class Post(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('name'))
    genitive = models.CharField(max_length=70, verbose_name=_('genitive'), default="")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['name']


class Organization(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=128, unique=True)
    full_name = models.TextField(verbose_name=_('full name'), null=True, blank=True)
    abbreviate = models.CharField(max_length=32, verbose_name=_('abbreviate'), unique=True)
    territory = models.ForeignKey(Territory, blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.abbreviate

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
        ordering = ['name']


class CertifyingCommissionMember(models.Model):
    first_name = models.CharField(max_length=32, verbose_name=_('first name'))
    last_name = models.CharField(max_length=32, verbose_name=_('last name'))
    middle_name = models.CharField(max_length=32, verbose_name=_('middle name'))
    post = models.CharField(max_length=128, verbose_name=_('post'))
    organization = models.CharField(max_length=512, verbose_name=_('organization'))
    request_form = models.CharField(max_length=96, verbose_name=_('appeal in request'))
    territory = models.ForeignKey(Territory, verbose_name=_('territory'), blank=True, null=True)

    def __unicode__(self):
        return '%s %s.%s.' % (self.last_name, self.first_name[0], self.middle_name[0])

    class Meta:
        verbose_name = _('certifying commission member')
        verbose_name_plural = _('certifying commission members')
        ordering = ['last_name', 'first_name', 'middle_name']


class CertifyingCommission(models.Model):
    creation_date = models.DateField(verbose_name=_('creation date'))
    expiration_date = models.DateField(verbose_name=_('expiration date'))
    name = models.CharField(max_length=512, verbose_name=_('name'), help_text=_('name in request'))
    members = models.ManyToManyField(CertifyingCommissionMember, verbose_name=_('members'))
    chairman = models.ForeignKey(CertifyingCommissionMember, verbose_name=_('chairman'), related_name='chairman',
                                 null=True, blank=True)
    vice_chairman = models.ForeignKey(CertifyingCommissionMember, verbose_name=_('vaice chairman'), related_name='vice',
                                      null=True, blank=True)
    secretary = models.ForeignKey(CertifyingCommissionMember, verbose_name=_('secretary'), related_name='secretary',
                                  null=True, blank=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.creation_date)

    class Meta:
        verbose_name = _('certifying commission')
        verbose_name_plural = _('certifying commisions')
        ordering = ['creation_date', 'expiration_date']


class Area(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('educational area')
        verbose_name_plural = _('educational areas')
        ordering = ['name']


class Expert(models.Model):
    first_name = models.CharField(verbose_name=_('first name'), max_length=32)
    last_name = models.CharField(verbose_name=_('last name'), max_length=32)
    middle_name = models.CharField(verbose_name=_('middle name'), max_length=32)
    post = models.CharField(max_length=256, verbose_name=_('post'))
    organization = models.TextField(verbose_name=_('organization'), null=True, blank=True)
    territory = models.ForeignKey(Territory, verbose_name=_('territory'))
    email = models.EmailField(verbose_name=_('email'), blank=True, null=True)
    area = models.ForeignKey(Area, verbose_name=_('educational area'))
    not_active = models.BooleanField(verbose_name=u'Не активен', default=False)

    organization_type = models.CharField(
        max_length=32, blank=True, null=True, choices=OTYPES, verbose_name=u'направление сертификации'
    )

    def __unicode__(self):
        return '%s %s.%s.' % (self.last_name, self.first_name[0], self.middle_name[0])

    class Meta:
        verbose_name = _('expert')
        verbose_name_plural = _('experts')
        ordering = ['last_name', 'first_name', 'middle_name']


#class Administrator(models.Model):
#    first_name = models.CharField(verbose_name=_('first name'), max_length=32)
#    last_name = models.CharField(verbose_name=_('last name'), max_length=32)
#    middle_name = models.CharField(verbose_name=_('middle name'), max_length=32)
#    post = models.ForeignKey(Post, verbose_name=_('post'))
#
#    def __unicode__(self):
#        return '%s %s.%s.' % (self.last_name, self.first_name[0], self.middle_name[0])
#
#    class Meta:
#        verbose_name = _('administrator')
#        verbose_name_plural = _('administrators')
#        ordering = ['last_name', 'first_name', 'middle_name']


class Qualification(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=64, unique=True)
    request_form = models.CharField(verbose_name=_('name in request'), max_length=64, unique=True)
    result_form = models.CharField(verbose_name=_('name in result'), max_length=64, null=True, blank=True)
    for_confirmation = models.BooleanField(verbose_name=_('for confirmation'), default=False)
    first = models.BooleanField(verbose_name=_('first category'), default=False)
    best = models.BooleanField(verbose_name=_('best category'), default=False)
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('qualification')
        verbose_name_plural = _('qualifications')
        ordering = ['name']


class Degree(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('degree')
        verbose_name_plural = _('degrees')
        ordering = ['name']


class AcademicTitle(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('academic title')
        verbose_name_plural = _('academic titles')
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('title')
        verbose_name_plural = _('titles')
        ordering = ['name']


class RequestStatus(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=32)
    is_new = models.BooleanField(verbose_name=_('is new'), default=False)
    is_rejected = models.BooleanField(verbose_name=_('is rejected'), default=False)
    is_in_expertise = models.BooleanField(verbose_name=_('is in expertize'), default=False)
    is_expertise_results_received = models.BooleanField(default=False, verbose_name=_('is expertise results received'))
    is_done = models.BooleanField(verbose_name=_('is done'), default=False)
    is_fail = models.BooleanField(default=False, verbose_name=_('is fail'))
    next_status = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('request status')
        verbose_name_plural = _('request statuses')
        ordering = ['name']


class Request(models.Model):
    first_name = models.CharField(max_length=32, verbose_name=_('first name'))
    last_name = models.CharField(max_length=32, verbose_name=_('last name'))
    middle_name = models.CharField(max_length=32, verbose_name=_('middle name'))
    genitive = models.CharField(max_length=96, verbose_name=_('genetive form of name'), default="")
    birth_date = models.DateField(verbose_name=_('birth date'))
    post = models.ForeignKey(Post, verbose_name=_('post'))
    discipline = models.CharField(max_length=64, verbose_name=_('discipline'), blank=True, null=True)
    post_date = models.DateField(verbose_name=_('date of appointment'))
    territory = models.ForeignKey(Territory, verbose_name=_('territory'), null=True, blank=True)
    organization = models.ForeignKey(Organization, verbose_name=_('organization'), null=True, blank=True)
    organization_name = models.CharField(max_length=512, verbose_name=_('organization name'), blank=True, null=True)
    qualification = models.ForeignKey(Qualification, verbose_name=_('qualification'))
    with_qualification = models.ForeignKey(Qualification, verbose_name=_('has qualification'), blank=True, null=True,
                                           related_name='request_has_set')
    expiration_date = models.DateField(verbose_name=_('expiration date'), blank=True, null=True)
    results = models.TextField(verbose_name=_('work results'))
    experience = models.IntegerField(verbose_name=_('experience'))
    pedagogical_experience = models.IntegerField(verbose_name=_('pedagogical experience'))
    post_experience = models.IntegerField(verbose_name=_('experience in post'))
    organization_experience = models.IntegerField(verbose_name=_('experience in organization'))
    degrees = models.ManyToManyField(Degree, verbose_name=_('degree'))
    academic_title = models.ForeignKey(AcademicTitle, verbose_name=_('academic title'), blank=True, null=True)
    presence = models.BooleanField(default=False, verbose_name=_('with personal presence'))
    email = models.EmailField(verbose_name=_('email'))
    official_email = models.EmailField(verbose_name=_('email'), null=True, blank=True, default=None)
    trainings = models.TextField(verbose_name=_('trainings'))
    experts = models.ManyToManyField(Expert, through='ExpertInRequest')
    phone = models.CharField(max_length=12, verbose_name=_('phone'), null=True, blank=True)
    secret_code = models.CharField(max_length=128, verbose_name=_('secret code'), unique=True)
    recomendations = models.TextField(verbose_name=_('recomendations'), blank=True, null=True)
    decision = models.TextField(verbose_name=_('decision'), blank=True, null=True)
    notes = models.TextField(verbose_name=_('notes'), blank=True, null=True)
    number_of_members = models.IntegerField(verbose_name=_('number of comission members'), null=True, blank=True)
    agree = models.IntegerField(verbose_name=_('agree'), null=True, blank=True)
    disagree = models.IntegerField(verbose_name=_('disagree'), null=True, blank=True)
    retrain = models.IntegerField(verbose_name=_('retrain'), null=True, blank=True)
    achievements = models.ManyToManyField(Achievement, verbose_name=_('achievments'))
    attestation_date = models.DateField(verbose_name=_('attestation date'), null=True, blank=True)
    order_date = models.DateField(verbose_name=_('order date'), null=True, blank=True)
    order_number = models.IntegerField(verbose_name=_('order number'), null=True, blank=True)

    doc_date = models.DateField(verbose_name=u'Дата получения документов', null=True, blank=True, default=None)
    doc_for_simple = models.CharField(max_length=512, verbose_name=u'Документ на право прохождение аттестации по УП',
                                      null=True, blank=True, default=None)

    status = models.ForeignKey(RequestStatus, blank=True, null=True)

    organization_type = models.CharField(
        max_length=32, blank=True, null=True, choices=OTYPES, verbose_name=u'направление сертификации'
    )

    @property
    def is_simple(self):
        return bool(self.doc_for_simple)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.secret_code:
            self.secret_code = sha1(datetime.datetime.today().isoformat()).hexdigest()

        super(Request, self).save(force_insert, force_update, using)

    def fio(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.middle_name)

    def __unicode__(self):
        return 'Request #%s' % self.id

    class Meta:
        verbose_name = _('request')
        verbose_name_plural = _('requests')
        ordering = ['id']


class Comment(models.Model):
    comment = models.TextField(verbose_name=_('comment'))
    request = models.ForeignKey(Request)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Comment %s for request %s" % (self.id, self.request_id)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['-time']


class ExpertInRequest(models.Model):
    expert = models.ForeignKey(Expert)
    request = models.ForeignKey(Request)
    first_grade = models.FloatField(verbose_name=_('first grade'), blank=True, null=True)
    second_grade = models.FloatField(verbose_name=_('second grade'), blank=True, null=True)
    auto_assigned = models.BooleanField(verbose_name=u'Назначен автоматически', default=False)

    class Meta:
        verbose_name = _('expert in request')
        verbose_name_plural = _('experts in request')
        ordering = ['expert__last_name']
        unique_together = ['expert', 'request']


class Education(models.Model):
    institution = models.CharField(max_length=512, verbose_name=_('institution'))
    diploma_year = models.IntegerField(verbose_name=_('diploma year'))
    speciality = models.CharField(max_length=128, verbose_name=_('speciality'))
    qualification = models.CharField(max_length=128, verbose_name=_('qualification'))
    request = models.ForeignKey(Request, verbose_name=_('request'))

    def __unicode__(self):
        return 'Education #%s' % self.id

    class Meta:
        verbose_name = _('education')
        verbose_name_plural = _('educations')
        ordering = ['id']


class RequestFlow(models.Model):
    request = models.ForeignKey(Request, verbose_name=_('request'))
    status = models.ForeignKey(RequestStatus, verbose_name=_('status'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))

    def __unicode__(self):
        return "%s: %s" % (self.request.__unicode__(), self.status.name)

    class Meta:
        verbose_name = _('request flow')
        verbose_name_plural = _('request flows')
        ordering = ['date']
        get_latest_by = 'date'


class Config(models.Model):
    start_date = models.DateField(verbose_name=_('start date'))
    end_date = models.DateField(verbose_name=_('end_date'))
    #max
    first_stage_max_grade = models.IntegerField(verbose_name=_('first stage max grade'), blank=True, null=True)
    second_stage_max_grade = models.IntegerField(verbose_name=_('second stage max grade'), blank=True, null=True)
    #min
    first_stage_min_grade = models.IntegerField(verbose_name=_('first stage min grade'))
    second_stage_min_grade = models.IntegerField(verbose_name=_('second stage min grade'))
    category = models.ForeignKey(Qualification, verbose_name=_('category'))
    is_child_organization = models.BooleanField(default=False, verbose_name=_('is for child organization'),
                                                help_text=_(
                                                    'Place mark if this config for child_organiation, remove mark otherwise'))

    def __unicode__(self):
        return _("Config for period") + " [%s-%s]" % (self.start_date.strftime('%x'), self.end_date.strftime('%x'))

    class Meta:
        verbose_name = _('config')
        verbose_name_plural = _('configs')
        ordering = ['-start_date']


class Criterion(models.Model):
    text = models.TextField(verbose_name=_('text'), unique=True)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = _('criterion')
        verbose_name_plural = _('criteria')
        ordering = ['id']


class Indicator(models.Model):
    text = models.TextField(verbose_name=_('text'), unique=True)
    cost = models.IntegerField(default=10, verbose_name=_('cost'))
    criterion = models.ForeignKey(Criterion)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = _('indicator')
        verbose_name_plural = _('indicators')
        ordering = ['id']


# Signals and slots -------------------------------------------------------------
#noinspection PyUnusedLocal
def status_changed_slot(sender, **kwargs):
    inst = kwargs['instance']

    lc = 'ru'
    if len(LANGUAGE_CODE) > 1:
        lc = LANGUAGE_CODE[0:2]

    txt_template = get_template('mail/%s/status_changed.txt' % lc)
    html_template = get_template('mail/%s/status_changed.html' % lc)
    c = {
        'rf': inst,
        'to_date': datetime.date.today() + datetime.timedelta(days=16)
    }

    msg = EmailMultiAlternatives(_('Status of your request has been changed'), txt_template.render(Context(c)),
                                 'att@iro86.ru', [inst.request.email])
    msg.attach_alternative(html_template.render(Context(c)), 'text/html')
    msg.send(fail_silently=not DEBUG)


#noinspection PyUnusedLocal
def expert_assigned_slot(sender, **kwargs):
    inst = kwargs['instance']
    if not inst.expert.email:
        return None

    lc = 'ru'
    if len(LANGUAGE_CODE) > 1:
        lc = LANGUAGE_CODE[0:2]

    txt_template = get_template('mail/%s/expert_assigned.txt' % lc)
    html_template = get_template('mail/%s/expert_assigned.html' % lc)

    c = {"eir": inst}

    msg = EmailMultiAlternatives(_('You assigned to expertise'), txt_template.render(Context(c)),
                                 'att@iro86.ruu', [inst.expert.email])
    msg.attach_alternative(html_template.render(Context(c)), 'text/html')
    msg.send(fail_silently=not DEBUG)


#noinspection PyUnusedLocal
def comment_added_slot(sender, **kwargs):
    inst = kwargs['instance']
    if not inst.request.email:
        return None

    lc = 'ru'
    if len(LANGUAGE_CODE) > 1:
        lc = LANGUAGE_CODE[0:2]

    txt_template = get_template('mail/%s/comment_added.txt' % lc)
    html_template = get_template('mail/%s/comment_added.html' % lc)

    c = {"comment": inst}

    msg = EmailMultiAlternatives(_('New comment'), txt_template.render(Context(c)),
                                 'att@iro86.ru', [inst.request.email])
    msg.attach_alternative(html_template.render(Context(c)), 'text/html')
    msg.send(fail_silently=not DEBUG)

# connections ------------------------------------------------------------------
post_save.connect(status_changed_slot, sender=RequestFlow, dispatch_uid='request_flow_created_email')
post_save.connect(expert_assigned_slot, sender=ExpertInRequest, dispatch_uid='expert_assigned_email')
post_save.connect(comment_added_slot, sender=Comment, dispatch_uid='comment_added_email')