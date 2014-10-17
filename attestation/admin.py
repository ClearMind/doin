from django.contrib import admin
from django.contrib.admin import  site
from attestation.models import *


class ExpertAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'territory', 'area', 'not_active')
    list_display_links = ('first_name', 'last_name', 'middle_name')
    list_filter = ('organization_type', 'area')
    search_fields = ('last_name', )
    list_editable = ['not_active']
    fields = [
        'last_name',
        'first_name',
        'middle_name',
        'post',
        'organization',
        'organization_type',
        'territory',
        'email',
        'area',
        'not_active'
    ]


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'category', 'is_child_organization')
    list_display_links = ('start_date', 'end_date', 'category', 'is_child_organization')
    list_filter = ('is_child_organization', 'category')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'territory')
    list_display_links = ('last_name', 'first_name', 'middle_name')
    search_fields = ('last_name', )
    fields = [
        'last_name',
        'first_name',
        'middle_name',
        'request_form',
        'post',
        'organization',
        'territory',
    ]


class CommissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'expiration_date')
    list_display_links = ('name', 'creation_date', 'expiration_date')
    filter_horizontal = ['members']

site.register(SettlementType)
site.register(Settlement)
site.register(Post)
site.register(Territory)
site.register(Degree)
site.register(AcademicTitle)
site.register(Qualification)
site.register(Organization)
site.register(RequestStatus)
site.register(Expert, ExpertAdmin)
site.register(Config, ConfigAdmin)
site.register(CertifyingCommission, CommissionAdmin)
site.register(CertifyingCommissionMember, MemberAdmin)
site.register(Area)
site.register(Achievement)
