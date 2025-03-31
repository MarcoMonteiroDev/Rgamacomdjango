from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from .models import Produto,Promo

# Create your views here.

class IndexView(ListView):
    template_name = "index.html"
    model = Produto
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["produtos"] = Produto.objects.all()
        context["promocoes"] = Promo.objects.all()
        return context

class ProdutoView(DetailView):
    template_name = "produto.html"
    model = Produto
    context_object_name = 'produto'