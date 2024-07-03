from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from mailing.forms import MailingForm, MassageForm, CustomersForm, MailingManagerForm
from mailing.models import Mailing, Customers, Massage, Mailing_attempt
from mailing.services import get_qs_from_cache


class MassageListView(ListView):
    model = Massage
    template_name = 'mailing/home.html'

    def get_queryset(self):
        return get_qs_from_cache(qs=Massage.objects.all(), key='massage_list')

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


class MassageCreateView(LoginRequiredMixin, CreateView):
    model = Massage
    form_class = MassageForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Massage, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        mailing_template = form.save()
        self.object = form.save()
        self.object.owner = self.request.user
        mailing_template.owner = self.object.owner
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            mailing_template.save()
        return super().form_valid(form)


class MassageUpdateView(LoginRequiredMixin, UpdateView):
    model = Massage
    form_class = MassageForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Massage, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingFormset(instance=self.object)
        return context_data

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MassageForm
        if user.is_staff:
            return MailingManagerForm
        raise PermissionDenied

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        massage_template = form.save()
        self.object = form.save()
        self.object.owner = self.request.user
        massage_template.owner = self.object.owner
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            massage_template.save()
        return super().form_valid(form)


class MassageDeleteView(LoginRequiredMixin, DeleteView):
    model = Massage
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"


def settings_toggle_active(request, pk):
    mailing_item = get_object_or_404(Mailing_attempt, pk=pk)
    if mailing_item.is_active is True:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True
        mailing_item.save()
    return redirect(reverse('mailing:home'))


class MassageDetailView(LoginRequiredMixin, DetailView):
    model = Massage
    template_name = 'mailing/massage_detail.html'
    login_url = "users:login"
    redirect_field_name = "redirect_to"


class CustomersCreateView(LoginRequiredMixin, CreateView):
    model = Customers
    form_class = CustomersForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        customer = form.save()
        user = self.request.user
        customer.owner = user
        customer.save()
        return super().form_valid(form)


class CustomersUpdateView(LoginRequiredMixin, UpdateView):
    model = Customers
    form_class = CustomersForm
    success_url = reverse_lazy('mailing:customers_list')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        customer = form.save()
        user = self.request.user
        customer.owner = user
        customer.save()
        return super().form_valid(form)


class CustomersDeleteView(LoginRequiredMixin, DeleteView):
    model = Customers
    success_url = reverse_lazy('mailing:customers_list')
    login_url = "users:login"
    redirect_field_name = "redirect_to"


class CustomersDetailView(DetailView):
    model = Customers
    template_name = 'mailing/customers_detail.html'
    login_url = "users:login"
    redirect_field_name = "redirect_to"


class CustomersListView(ListView):
    model = Customers
    template_name = 'mailing/customers_list.html'

    def get_queryset(self):
        return get_qs_from_cache(qs=Customers.objects.all(), key='customers_list')

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
