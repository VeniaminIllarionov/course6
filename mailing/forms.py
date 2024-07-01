from django import forms
from django.forms import BooleanField

from mailing.models import Mailing, Massage, Customers

words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')


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


class MassageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Massage
        fields = '__all__'

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('massage', 'subject_massage', )

        if cleaned_data in words:
            raise forms.ValidationError('Возникла ошибка')
        return cleaned_data


class CustomersForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('email', 'fio', 'comment',)

        if cleaned_data in words:
            raise forms.ValidationError('Возникла ошибка ')
        return cleaned_data
