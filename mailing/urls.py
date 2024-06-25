from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (contacts, ProductDetailView, ProductListView, ProductCreateView, ProductUpdateView,
                           ProductDeleteView, CategoryListView)

app_name = MailingConfig.name

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create'),
    path('', ProductListView.as_view(), name='home'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('contact/', contacts, name='contact'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('category/', CategoryListView.as_view(), name='category'),]
