from django.contrib import admin

from mailing.models import Mailing, Massage, Mailing_attempt, Customers
from users.models import User


# Register your models here.
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_id',)
    list_filter = ('mailing_id',)
    search_fields = ('mailing_id',)


@admin.register(Massage)
class MassageAdmin(admin.ModelAdmin):
    list_display = ('mailing_id', 'subject_massage', 'massage',)
    list_filter = ('mailing_id',)
    search_fields = ('subject_massage', 'massage',)


@admin.register(Mailing_attempt)
class Mailing_attemptAdmin(admin.ModelAdmin):
    list_display = ('last_attempt', 'status', 'mail_response',)
    list_filter = ('mailing_id',)
    search_fields = ('mailing_id',)


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('email', 'fio', 'comment',)
    list_filter = ('mailing_id',)
    search_fields = ('mailing_id',)


@admin.register(User)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'country')
    list_filter = ('email',)
    search_fields = ('email',)
