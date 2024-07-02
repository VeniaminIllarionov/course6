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
        fields = ('frequency',)

    def clean_massage(self):
        cleaned_data = self.cleaned_data.get('massage', )

        if cleaned_data in words:
            raise forms.ValidationError('Возникла ошибка сообщении')
        return cleaned_data


class MassageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Massage
        exclude = ('owner',)

    def clean_massage(self):
        cleaned_data = self.cleaned_data.get('massage', )

        if cleaned_data in words:
            raise forms.ValidationError('Возникла ошибка сообщении')
        return cleaned_data


class CustomersForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Customers
        exclude = ('owner',)

    def clean_comment(self):
        cleaned_data = self.cleaned_data.get('comment', )

        if cleaned_data in words:
            raise forms.ValidationError('Возникла ошибка в описании ')
        return cleaned_data

    def clean_fio(self):
        cleaned_data = self.cleaned_data.get('fio', )

        if cleaned_data in words:
            raise forms.ValidationError('Возникла ошибка в ФИО')
        return cleaned_data
