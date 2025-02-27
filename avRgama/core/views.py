from django.shortcuts import render
from .models import Produto

# Create your views here.

def index(request):
    context = {
        "produtos": Produto.objects.all()
    }

    return render(request, "index.html", context)

def produto(request,pk):

    prod = Produto.objects.get(id=pk)

    context = {
        "produto": prod ,
    }

    return render(request, "produto.html", context)