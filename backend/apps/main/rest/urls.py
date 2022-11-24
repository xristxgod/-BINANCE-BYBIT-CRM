from django.urls import path, include

from rest_framework.routers import SimpleRouter

import apps.main.rest.views as views


urlpatterns = [
    path(r'accounts/', views.AccountsView.as_view(), name='accounts'),
]