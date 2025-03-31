from django.contrib import admin
from .models import Produto, Promo
# Register your models here.

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "descricao", "estoque", "slug", "criado", "modificado", "ativo")

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ("nome","imagem_promo")