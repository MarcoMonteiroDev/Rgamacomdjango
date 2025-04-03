from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from .models import Produto,Promo
# Create your views here.

class IndexView(ListView):
    template_name = "index.html"
    model = Produto
    paginate_by = 30

    def get_queryset(self):
        categoria = self.request.GET.get("categoria")
        queryset = Produto.objects.all()

        if categoria:
            queryset = queryset.filter(categoria__iexact=categoria)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["produtos"] = self.object_list
        context["promocoes"] = Promo.objects.all()
        context["categorias"] = Produto.CAT_CHOICES
        context["categoria_selecionada"] = self.request.GET.get("categoria","") #para usar no if para deixar a cat selecionada preta
        
        return context

class ProdutoView(DetailView):
    template_name = "produto.html"
    model = Produto
    context_object_name = 'produto'