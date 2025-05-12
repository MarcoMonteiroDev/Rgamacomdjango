from django.contrib import admin
from .models import Produto, Promo, Carrinho
# Register your models here.

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "descricao", "estoque", "slug", "criado", "modificado", "ativo")

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ("nome","imagem_promo")

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id',"chave_sessao","usuario_nome")
    search_fields = ("user__username","user__email,")

    def usuario_nome(self, obj):
        return obj.user.email if obj.user else 'Anônimo'
    usuario_nome.short_description = 'Usuário'
