from django.urls import path,include
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("teste",TemplateView.as_view(template_name="teste.html"),name="teste" ),
]