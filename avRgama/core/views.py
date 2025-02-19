from django.shortcuts import render
from .models import Produto

# Create your views here.

def index(request):
    context = {
        "produtos": Produto.objects.all()
    }

    return render(request, "index.html", context)