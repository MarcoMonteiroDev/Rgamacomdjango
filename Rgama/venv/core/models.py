from django.db import models
from stdimage.models import StdImageField
from django.db.models import signals
from django.template.defaultfilters import slugify
from django.conf import settings
from django.utils import timezone
import uuid

def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)

def get_file_path(_instance, filename):
    ext = filename.split(".")[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

class Base(models.Model):
    criado = models.DateField("Data de Criação", auto_now_add=True)
    modificado = models.DateField("Data de Atualização", auto_now=True)
    ativo = models.BooleanField("Ativo?",default=True)
    
    class Meta:
        abstract = True

class Produto(Base):
    CAT_CHOICES = (
        ("MDC", 'Materiais de Construção'),
        ("TEA", 'Tintas e Acessorios'),
        ("PER", 'Pisos e Revestimentos'),
        ("EAC", 'Eletrico e Acabamento'),
        
    )

    MEDIDA_CHOICES = (
        ("M\u00b2", "Metro Quadrados"),
        ("M", "Metros"),
        ("MM", "Milimetros"),
        ("CM","Centimetros"),
        ("L","Litros")
    )

    nome = models.CharField("Nome", max_length=40)
    preco = models.DecimalField("Preço",max_digits=8, decimal_places=2)
    descricao = models.TextField("Descrição", max_length=150)
    estoque = models.DecimalField("Estoque", max_digits=8, decimal_places=2)
    categoria = models.CharField("Categoria", max_length=40, choices=CAT_CHOICES, default= "materiais de construcao")
    medida = models.CharField("Medida", max_length=20, choices=MEDIDA_CHOICES, default="M")
    imagem = StdImageField("Imagem", upload_to='produtos', variations={"thumb": (224,224)})
    slug = models.SlugField("Slug", max_length=100, blank=True, editable=False)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

class Promo(Base):
    nome = models.CharField("Nome",max_length=40)
    imagem_promo = StdImageField("Promo", upload_to="promocoes", variations={"thumb":(1536,512)})
    slug = models.SlugField("Slug",max_length=100, blank=True, editable=False)
    
    def __str__(self):
        return self.nome

class Carrinho(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    chave_sessao = models.CharField(max_length=40, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f"Carrinho #{self.id}"

class ItemCarrinho(Base):
    carrinho = models.ForeignKey(Carrinho, related_name="itens", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantidade * self.produto.preco

class Pedido(Base):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    endereco = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.pk} - {self.nome}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.nome}"


signals.pre_save.connect(produto_pre_save, sender=Produto)
signals.pre_save.connect(produto_pre_save, sender=Promo)