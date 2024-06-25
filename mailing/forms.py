from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version, Category

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


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('is_published',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')

        if cleaned_data in words:
            raise forms.ValidationError('Возникла ошибка в Наименовании')
        return cleaned_data


class ProductManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'is_published', 'category')

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')

        if cleaned_data in words:
            raise forms.ValidationError('Возникла ошибка в Наименовании')
        return cleaned_data


def clean_description(self):
    cleaned_data = self.cleaned_data.get('description')

    if cleaned_data in words:
        raise forms.ValidationError('Возникла ошибка в Описании')
    return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


class CategoryForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
