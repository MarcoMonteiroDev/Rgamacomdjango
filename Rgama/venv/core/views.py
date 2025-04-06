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
        categoria = self.request.GET.get("categoria") # aqui ele pega o valor passado para a url pelo metodo request la no ancora quando passo ?categoria=value
        busca = self.request.GET.get("busca")
        queryset = Produto.objects.all()

        if categoria:
            queryset = queryset.filter(categoria__iexact=categoria) #categoria_iexact = case-insensitive exact match para evitar erro de case sensitive

        if busca:
            queryset = queryset.filter(nome__icontains=busca)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["produtos"] = self.object_list #traz a lista do query set
        context["promocoes"] = Promo.objects.all()
        context["categorias"] = Produto.CAT_CHOICES #para trazer as categorias para serem usadas no laço de repetição
        context["categoria_selecionada"] = self.request.GET.get("categoria","") #para usar no if para deixar a cat selecionada preta retorna o valor associado a categoria categoria=valor se nao houver retorna vazio
        
        return context

class ProdutoView(DetailView):
    template_name = "produto.html"
    model = Produto
    context_object_name = 'produto'

    def get_context_data(self, **kwargs):
        context = super(ProdutoView,self).get_context_data(**kwargs)
        context["categorias"] = Produto.CAT_CHOICES #para trazer as categorias para serem usadas no laço de repetição
        return context