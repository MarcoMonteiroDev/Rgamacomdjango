from django.db import models
from stdimage.models import StdImageField
from django.db.models import signals
from django.template.defaultfilters import slugify
import uuid

def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)

def get_file_path(_instance, filename):
    ext = filename.split("."[-1])
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
        ("materiais de construcao", 'Materiais de Construção'),
        ("tintas e acessorios", 'Tintas e Acessorios'),
        ("pisos e revestimentos", 'Pisos e Revestimentos'),
        ("eletrico e acabamento", 'Eletrico e Acabamento'),
        
    )

    MEDIDA_CHOICES = (
        ("M\u00b2", "Metro Quadrados"),
        ("M", "Metros"),
        ("MM", "Milimetros"),
        ("CM","Centimetros"),
        ("L","Litros")
    )

    nome = models.CharField("Nome", max_length=80)
    preco = models.DecimalField("Preço",max_digits=8, decimal_places=2)
    descricao = models.TextField("Descrição", max_length=150)
    estoque = models.DecimalField("Estoque", max_digits=8, decimal_places=2)
    categoria = models.CharField("Categoria", max_length=40, choices=CAT_CHOICES, default= "materiais de construcao")
    medida = models.CharField("Medida", max_length=20, choices=MEDIDA_CHOICES, default="metros")
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
    


signals.pre_save.connect(produto_pre_save, sender=Produto)
signals.pre_save.connect(produto_pre_save, sender=Promo)