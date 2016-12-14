# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from .forms import TesisForm


class TesisFormView(FormView):
    form_class = TesisForm
    template_name = 'tesis_form.html'

    def form_valid(self, form):
        valor_analizador = form.cleaned_data['analizador']
        valor_texto = form.cleaned_data['texto']
        return super(TesisFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('inicio')