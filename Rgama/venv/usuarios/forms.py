from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUsuario

class CustomUsuarioCreateForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name','fone','email')
        labels = {"username": "Username/E-mail"}

        def save(self, commit=True):
            user = super().save(commit=True)
            user.set_password(self.cleaned_data['password1'])
            user.username = self.cleaned_data.get('email')
            
            if commit:
                user.save()
            return user
        
class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name','fone')