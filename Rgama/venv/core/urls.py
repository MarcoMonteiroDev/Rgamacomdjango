from django.urls import path
from .views import IndexView, ProdutoView, Busca_Produtos, CarrinhoView, AdicionarAoCarrinho, RemoverDoCarrinho, VerCarrinhoView, AtualizarQuantidade, CheckOutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path("", IndexView.as_view(), name="index"),
    path("produto/<int:pk>", ProdutoView.as_view() , name="produto"),
    path("buscar/",Busca_Produtos.as_view(),name="busca_produtos"),
    path("carrinho/",VerCarrinhoView.as_view(),name="carrinho"),
    path("carrinho/add/<int:produto_id>", AdicionarAoCarrinho.as_view(),name="adicionar_carrinho"),
    path("carrinho/rmv/<int:produto_id>", RemoverDoCarrinho.as_view(),name="remover_carrinho"),
    path("carrinho/atl/", AtualizarQuantidade.as_view(),name="atualizar_quantidade"),
    path("checkout/", CheckOutView.as_view(),name="checkout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)