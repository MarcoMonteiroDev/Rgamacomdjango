from django.urls import path,include
from django.views.generic.base import TemplateView
from .views import CadastroView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("cadastro", CadastroView.as_view(), name="cadastro"),
]