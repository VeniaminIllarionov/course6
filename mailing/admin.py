from django.contrib import admin

from mailing.models import Mailing, Massage, Mailing_attempt, Customers
from users.models import User


# Register your models here.
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'frequency', 'mailing_status',)
    list_filter = ('mailing_status',)
    search_fields = ('mailing_status',)


@admin.register(Massage)
class MassageAdmin(admin.ModelAdmin):
    list_display = ('subject_massage', 'massage', )
    list_filter = ('subject_massage',)
    search_fields = ('subject_massage', 'massage',)


@admin.register(Mailing_attempt)
class Mailing_attemptAdmin(admin.ModelAdmin):
    list_display = ('last_attempt', 'status', 'is_active',)
    list_filter = ('status',)
    search_fields = ('status',)


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('email', 'fio', 'comment',)
    list_filter = ('email',)
    search_fields = ('email',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'country', 'is_block',)
    list_filter = ('email',)
    search_fields = ('email',)
