from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, RedirectView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Produto, Promo, Carrinho, ItemCarrinho, Pedido, ItemPedido
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from decimal import Decimal
from django.contrib import messages
import json, re


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
        # Garante que a sessão esteja ativa
        if not self.request.session.session_key:
            self.request.session.create()

        produto = get_object_or_404(Produto, id=self.kwargs["produto_id"])
        quantidade = int(self.request.POST.get("quantidade", 1))

        # Obtém o carrinho da sessão ou cria um novo dicionário
        carrinho = self.request.session.get("carrinho", {})
        produto_id = str(produto.id)  # Sempre usar string como chave de dicionário em JSON/session
        quantidade_existente = carrinho.get(produto_id,{}).get("quantidade", 0)

        quantidade_total = quantidade_existente + quantidade

        if quantidade_total > produto.estoque:
            messages.error(
                self.request,f"Não há estoque suficiente para '{produto.nome}'. Estoque disponível: {produto.estoque}."
            )
            return self.request.POST.get("next") or f"/produto/{produto.id}/"
        else:
            # Garante que o item seja adicionado corretamente
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
            return self.request.POST.get("next") or "/carrinho/"
    
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

        return HttpResponseRedirect("/checkout/")

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

class CheckOutView(TemplateView):
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho = self.request.session.get("carrinho",{})

        total = 0
        for item in carrinho.values():
            subtotal = item["quantidade"] * item["preco"]
            item["subtotal"] = round(subtotal, 2)
            total += subtotal

        context["carrinho"] = carrinho
        context["total"] = round(total, 2)
        return context

    def post(self, request, *args, **kwargs):
        carrinho = request.session.get("carrinho", {})
        if not carrinho:
            return redirect("/carrinho/")

        # Pega os dados do formulário
        nome = request.POST.get("nome")
        telefone = request.POST.get("telefone")
        endereco = request.POST.get("endereco")
        complemento = request.POST.get("complemento")

        if not re.match(r'^\(\d{2}\) \d{5}-\d{4}$', telefone):
            messages.error(request, "Telefone inválido. Use o formato (99)99999-9999.")
            return redirect("/checkout/")  # Voltar para o formulário

        # Validação de campos obrigatórios
        if not nome or not endereco or not telefone:
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect("/checkout/")

        total = sum(item["quantidade"] * item["preco"] for item in carrinho.values())

        pedido = Pedido.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            nome=nome,
            telefone=telefone,
            endereco=endereco,
            complemento=complemento,
            total=round(Decimal(total), 2)
        )

        for produto_id, item in carrinho.items():
            try:
                produto = Produto.objects.get(id=produto_id)
            except Produto.DoesNotExist:
                continue

            # Atualiza estoque antes de salvar ItemPedido (importante)
            if produto.estoque >= item["quantidade"]:
                produto.estoque -= item["quantidade"]
                produto.save()
            else:
                messages.error(request, f"Estoque insuficiente para o produto {produto.nome}.")
                pedido.delete()  # opcional, para cancelar o pedido se falhar
                return redirect("/checkout/")

            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                nome=item["nome"],
                quantidade=item["quantidade"],
                preco_unitario=item["preco"],
                subtotal=round(Decimal(item["quantidade"] * item["preco"]), 2)
            )

        
        request.session["carrinho"] = {}
        request.session.modified = True
        print("pedido feito com sucesso")
        return HttpResponseRedirect("/carrinho/")

class PedidosView(LoginRequiredMixin, ListView):
    template_name = "pedidos.html"
    model = "pedido"
    context_object_name = "pedidos"
    ordering = ['-criado']

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by('-criado_em')