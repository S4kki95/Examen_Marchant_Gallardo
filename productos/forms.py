from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ProductoForm(forms.ModelForm):
    class Meta: 
        model = Producto
        fields = [ 'objeto', 'marca', 'modelo', 'categoria', 'imagen']
        labels = {
            'objeto': 'Objeto',
            'marca' : 'Marca',
            'modelo' : 'Modelo',
            'categoria' : 'Categoria', 
            'imagen': 'Imagen'
        }
        widgets ={
            'objeto': forms.TextInput(
                attrs={
                    'placeholder':'Ingrese el objeto..',
                    'id': 'objeto',
                    'class': 'form-control'
                }
            ),
            'marca': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese marca..',
                    'id': 'marca',
                    'class': 'form-control'
                }
            ),
            'modelo': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese modelo..',
                    'id': 'modelo',
                    'class': 'form-control'
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'id': 'categoria',
                    'class': 'form-control'
                }
            ), 
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id': 'imagen',
                }
            )
            
        }