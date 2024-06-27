from django import forms
from django.forms import BooleanField

from mailing.models import Mailing, Massage, Customers


class StyleFormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('mailing_status',)


class MailingManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('frequency',)


class MassageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Massage
        fields = '__all__'


class CustomersForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'

