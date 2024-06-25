from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ProductForm, VersionForm, ProductManagerForm, CategoryForm
from mailing.models import Mailing, Customers, Massage, Mailing_attempt
from mailing.services import get_qs_from_cache


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/home.html'

    def get_queryset(self):
        return get_qs_from_cache(qs=Mailing.objects.all(), key='mailings_list')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'У вас новое сообщение: {name}({phone}): {message}')
    return render(request, 'mailing/contacts.html')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        self.object = form.save()
        user = self.request.user
        self.object.owner = user
        self.object.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('mailing.set_published') and user.has_perm('mailing.can_edit_description') and user.has_perm(
                'mailing.can_edit_category'):
            return ProductManagerForm
        raise PermissionDenied

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'mailing/product_detail.html'
    login_url = "users:login"
    redirect_field_name = "redirect_to"


class CategoryListView(ListView):
    model = Category
    template_name = 'mailing/category_list.html'

    def get_queryset(self):
        return get_qs_from_cache(qs=Category.objects.all(), key='categories_list')


from django.shortcuts import render

# Create your views here.
