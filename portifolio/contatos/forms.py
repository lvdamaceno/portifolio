from django import forms

class Contato(forms.Form):
    name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Nome', 'required': True}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(label='Telefone', widget=forms.TextInput(attrs={'placeholder': 'Telefone'}))
    message = forms.CharField(label='Mensagem', widget=forms.Textarea(attrs={'placeholder': 'Mensagem', 'rows': '3'}))