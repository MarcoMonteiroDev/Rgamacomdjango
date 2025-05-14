from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, RedirectView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Produto, Promo, Carrinho, ItemCarrinho
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
import json


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
    
class AdicionarAoCarrinho(LoginRequiredMixin, RedirectView):
    login_url = '/conta/login/'

    def get_redirect_url(self, *args, **kwargs):
        produto = get_object_or_404(Produto, id=self.kwargs["produto_id"])
        quantidade = int(self.request.POST.get("quantidade", 1))

        # Obtém o carrinho da sessão ou cria um novo dicionário
        carrinho = self.request.session.get("carrinho", {})

        produto_id = str(produto.id)  # Sempre usar string como chave de dicionário em JSON/session

        if produto_id in carrinho:
            carrinho[produto_id]["quantidade"] += quantidade
        else:
            carrinho[produto_id] = {
                "nome": produto.nome,
                "preco": float(produto.preco),  # Decimal não é serializável em JSON
                "quantidade": quantidade,
                "imagem": produto.imagem.url if produto.imagem else "",
            }

        # Salva o carrinho de volta na sessão
        self.request.session["carrinho"] = carrinho
        self.request.session.modified = True  # Garante que a sessão seja salva

        # Redireciona para próxima página
        next_url = self.request.POST.get("next") or "/carrinho/"
        return next_url
    
class RemoverDoCarrinho(View):
    def post(self, request, *args, **kwargs):
        produto_id = str(self.kwargs["produto_id"])  # garantir que seja string
        carrinho = request.session.get("carrinho", {})

        if produto_id in carrinho:
            del carrinho[produto_id]
            request.session["carrinho"] = carrinho
            request.session.modified = True

        return HttpResponseRedirect("/carrinho/")

class AtualizarQuantidade(View):
     def post(self, request, *args, **kwargs):
        carrinho = request.session.get("carrinho", {})

        for produto_id in carrinho.keys():
            campo_quantidade = f"quantidade_{produto_id}"
            nova_quantidade = int(request.POST.get(campo_quantidade, carrinho[produto_id]["quantidade"]))
            carrinho[produto_id]["quantidade"] = max(nova_quantidade, 1)

        request.session["carrinho"] = carrinho
        request.session.modified = True

        return HttpResponseRedirect("/carrinho/")

class VerCarrinhoView(TemplateView):
    template_name= "carrinho.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        carrinho = self.request.session.get("carrinho",{})

        total = 0
        for item in carrinho.values():
            subtotal = item["quantidade"] * item["preco"]
            item["subtotal"] = round(subtotal,2)
            total += subtotal

        context["carrinho"] = carrinho
        context["total"] = round(total, 2)
        return context