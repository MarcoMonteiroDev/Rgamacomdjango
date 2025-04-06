from django.urls import path
from .views import IndexView, ProdutoView, Busca_Produtos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path("", IndexView.as_view(), name="index"),
    path("produto/<int:pk>", ProdutoView.as_view() , name="produto"),
    path("buscar/",Busca_Produtos.as_view(),name="busca_produtos"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)