from django.shortcuts import render
from django.views.generic import CreateView
from .forms import CustomUsuarioCreateForm
from .models import CustomUsuario
from django.urls import reverse_lazy

# Create your views here.
class CadastroView(CreateView):
    template_name = "cadastro.html"
    form_class = CustomUsuarioCreateForm
    model = CustomUsuario
    success_url = reverse_lazy("login")