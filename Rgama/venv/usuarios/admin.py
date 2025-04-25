from django.contrib import admin
from .models import CustomUsuario

@admin.register(CustomUsuario)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','fone')