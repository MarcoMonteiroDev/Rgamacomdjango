from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, RedirectView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Produto, Promo, Carrinho, ItemCarrinho
from django.http import JsonResponse


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
        context["categoria_selecionada"] = self.request.GET.get("categoria","") #para usar no if para deixar a cat selecionada preta / retorna o valor associado a categoria categoria=valor se nao houver retorna vazio
        
        return context

class ProdutoView(DetailView):
    template_name = "produto.html"
    model = Produto
    context_object_name = 'produto'

    def get_context_data(self, **kwargs):
        context = super(ProdutoView,self).get_context_data(**kwargs)
        context["categorias"] = Produto.CAT_CHOICES #para trazer as categorias para serem usadas no laço de repetição
        return context

class Busca_Produtos(View):

    def get(self, request):
        termo = request.GET.get("bd","")# bd = busca dinamica
        produtos = Produto.objects.filter(nome__icontains = termo)[:5]

        data = []
        for p in produtos:
            data.append({
                "id":p.id,
                "nome":p.nome,
                "preco":p.preco,
                "imagem":p.imagem.url
            })

        return JsonResponse({"resultados": data})

class CarrinhoView(TemplateView):
    template_name = "detalhes_carrinho.html"

    def get_carrinho(self):
        chave_sessao = self.request.session.session_key
        if not chave_sessao:
            self.request.session.create()

        carrinho, created = Carrinho.objects.get_or_create(chave_sessao=self.request.session.session_key)
        return carrinho
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho = self.get_carrinho
        context["carrinho"] = carrinho

        return context
    
class AdicionarAoCarrinho(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        produto = get_object_or_404(Produto, id=self.kwargs["produto_id"])
        carrinho, _ = Carrinho.objects.get_or_create(chave_sessao=self.request.session.session_key)
        quantidade = int(self.request.POST.get("quantidade", 1))
        print(f"Quantidade recebida: {quantidade}")  # Verifique no console
        """   created retorna booleano se o item foi criado agora ou nao """
        item, created = ItemCarrinho.objects.get_or_create(carrinho = carrinho, produto = produto)
        """  se nao foi criado agora e porque ja existe """
        if not created:
            item.quantidade += quantidade
        else:
            item.quantidade = quantidade

        item.save()

        next_url = self.request.POST.get("next") or "/carrinho/"
        return next_url
    
class RemoverDoCarrinho(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(ItemCarrinho, id=self.kwargs["item_id"])
        item.delete()

        return "/carrinho/"