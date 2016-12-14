# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from django import forms

class TesisForm(forms.Form):
    OPCIONES_ANALIZADOR = (
        ('Stanford', 'Stanford'),
        ('Bikel', 'Bikel'),
    )

    texto = forms.CharField()
    analizador = forms.ChoiceField(choices=OPCIONES_ANALIZADOR, label="Seleccionar analizador")

    def __init__(self, *args, **kwargs):
        super(TesisForm, self).__init__(*args, **kwargs)
        self.fields['texto'].widget = forms.Textarea()
