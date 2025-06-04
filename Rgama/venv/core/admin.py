from django.contrib import admin
from .models import Produto, Promo, Carrinho, ItemCarrinho, Pedido, ItemPedido

# Register your models here.

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "descricao", "estoque", "slug", "criado", "modificado", "ativo")

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ("nome","imagem_promo")

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('produto', 'nome', 'quantidade', 'preco_unitario', 'subtotal')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'telefone', 'total_formatado', 'criado_em']
    readonly_fields = ['total']
    inlines = [ItemPedidoInline]  # <--- Isso exibe os itens do pedido dentro do admin
    search_fields = ['nome', 'telefone']
    list_filter = ['criado_em']

    def total_formatado(self, obj):
        return f"R$ {obj.total:.2f}"
    total_formatado.short_description = 'Total'
