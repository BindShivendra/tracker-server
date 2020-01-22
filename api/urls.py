from django.urls import path, include

from account.views import get_token

urlpatterns = [
    path('accounts/', include('account.urls')),
    path('get-token/', get_token, name='get_token'),
]
