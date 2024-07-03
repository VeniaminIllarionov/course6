from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (MassageDetailView, MailingListView, MassageCreateView, MassageUpdateView,
                           MassageDeleteView, CustomersCreateView, CustomersUpdateView, CustomersDetailView,
                           CustomersListView, CustomersDeleteView)

app_name = MailingConfig.name

urlpatterns = [
    path('create_mailing/', MassageCreateView.as_view(), name='create'),
    path('create_custom/', CustomersCreateView.as_view(), name='create_custom'),
    path('edit_custom/<int:pk>/', CustomersUpdateView.as_view(), name='edit_custom'),
    path('customers/<int:pk>/', CustomersDetailView.as_view(), name='customers_detail'),
    path('delete_custom/<int:pk>/', CustomersDeleteView.as_view(), name='delete_custom'),
    path('customers_list/', CustomersListView.as_view(), name='customers_list'),
    path('', MailingListView.as_view(), name='home'),
    path('edit/<int:pk>/', MassageUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', MassageDeleteView.as_view(), name='delete'),
    path('mailing/<int:pk>/', cache_page(60)(MassageDetailView.as_view()), name='mailing_detail'),
    ]
