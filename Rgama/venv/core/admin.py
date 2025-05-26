from django.contrib import admin
from .models import Produto, Promo, Carrinho, Pedido

# Register your models here.

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "descricao", "estoque", "slug", "criado", "modificado", "ativo")

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ("nome","imagem_promo")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'email', 'total_formatado', 'criado_em']
    readonly_fields = ['total']

    def total_formatado(self, obj):
        return f"R$ {obj.total:.2f}"
    total_formatado.short_description = 'Total'
