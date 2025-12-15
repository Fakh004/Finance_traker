from django.urls import path
from .views import *

urlpatterns = [
    path('', get_transaction, name='get_transaction'),
    path('add/', add_transaction, name='add-transaction'),
    path('<int:pk>/', transaction_detail, name='transaction_detail'),
    path('<int:pk>/edit/', transaction_edit, name='edit-transaction'),
    path('<int:pk>/delete/', delete_transaction, name='delete-transaction'),
    path('all/', transaction_list, name='transaction_list'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit-profile'),
]