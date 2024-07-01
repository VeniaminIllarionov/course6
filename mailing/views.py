from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm, MassageForm, CustomersForm
from mailing.models import Mailing, Customers, Massage, Mailing_attempt
from mailing.services import get_qs_from_cache


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/home.html'

    def get_queryset(self):
        return get_qs_from_cache(qs=Mailing.objects.all(), key='mailings_list')

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


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        massage_formset = inlineformset_factory(Mailing, Massage, form=MassageForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = massage_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = massage_formset(instance=self.object)
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


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MassageFormset = inlineformset_factory(Mailing, Massage, form=MassageForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MassageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MassageFormset(instance=self.object)
        return context_data

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


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
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


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
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
    success_url = reverse_lazy('mailing:home')
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
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"


class CustomersDetailView(DetailView):
    model = Customers
    template_name = 'mailing/customers_detail.html'
    login_url = "users:login"
    redirect_field_name = "redirect_to"
