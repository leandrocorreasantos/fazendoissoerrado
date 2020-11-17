# coding: utf-8
from django import forms


class ContatoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ContatoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            placeholder = '{}'
            if visible.field.required:
                placeholder = '{} *'
            visible.field.widget.attrs['placeholder'] = placeholder.format(
                visible.name.title()
            )

    nome = forms.CharField(required=True)
    email = forms.CharField(required=True)
    telefone = forms.CharField(required=False)
    mensagem = forms.CharField(widget=forms.Textarea, required=True)
