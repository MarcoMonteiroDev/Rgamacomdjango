from django.urls import path
from .views import IndexView, ProdutoView

urlpatterns =[
    path("", IndexView.as_view(), name="index"),
    path("produto/<int:pk>", ProdutoView.as_view() , name="produto"),
]