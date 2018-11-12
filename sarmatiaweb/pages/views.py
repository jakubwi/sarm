from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from pages.models import Rekrutacja, Klasa
from rejestracja.models import Podanie
from pages.forms import RekrutacjaForm, TworzenieKlasyForm, RekrutacjaNowaForm


def HomePageView(request):
    class_list = Klasa.objects.order_by('name')

    context_dict = {'class_list': class_list, }
    response = render(request, 'home.html', context=context_dict)
    return response

class RekrutacjaListView(ListView):
    template_name = 'rekrutacja_lista.html'
    model = Rekrutacja

class RekrutacjaUpdateView(UpdateView):
    model = Rekrutacja
    template_name = 'rekrutacja_update.html'
    form_class = RekrutacjaForm
    success_url = reverse_lazy('rekrutacja_lista')

class KlasaCreateView(CreateView):
    template_name = 'rejestracja/klasa_create.html'
    model = Klasa
    form_class = TworzenieKlasyForm
    
    def get_success_url(self):
        return reverse('rekrutacja_create', args=(self.object.pk,))

class RekrutacjaCreateView(CreateView):
    template_name = 'rekrutacja_create.html'
    model = Rekrutacja
    form_class = RekrutacjaNowaForm
    success_url = reverse_lazy('home')

class KlasaListView(ListView):
    model = Klasa
    template_name = 'rejestracja/klasa_lista.html'

class KlasaDeleteView(DeleteView):
    template_name = 'rejestracja/klasa_delete.html'
    model = Klasa
    success_url = reverse_lazy('panel_moda')

