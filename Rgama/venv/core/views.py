from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import Produto

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["produtos"] = Produto.objects.all()
        return context

class ProdutoView(DetailView):
    model = Produto
    template_name = "produto.html"
    context_object_name = 'produto'

