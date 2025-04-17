from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUsuario

class CustomUsuarioCreateForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name','fone','email')
        labels = {"username": "Username/E-mail"}

class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name','fone')