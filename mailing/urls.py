from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (MailingDetailView, MailingListView, MailingCreateView, MailingUpdateView,
                           MailingDeleteView)

app_name = MailingConfig.name

urlpatterns = [
    path('create/', MailingCreateView.as_view(), name='create'),
    path('', MailingListView.as_view(), name='home'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
    path('product/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='product_detail'),]
