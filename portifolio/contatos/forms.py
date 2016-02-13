from django import forms
import django
if django.VERSION < (1,7):
    from charsleft_widget.fields import CharField
else:
    from django.forms.fields import CharField

from charsleft_widget import CharsLeftArea


class Contato(forms.Form):
    name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Nome', 'required': True}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(label='Telefone', widget=forms.TextInput(attrs={'placeholder': 'Telefone'}))
    message = forms.CharField(max_length=150, label='Mensagem', widget=forms.Textarea(attrs={'placeholder': 'Mensagem', 'rows': '3'}))