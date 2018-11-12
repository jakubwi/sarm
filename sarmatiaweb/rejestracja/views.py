from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from rejestracja.models import Serwer, Rasa, Rola, Podanie, PodanieKomentarze
from rejestracja.forms import PodanieRaidForm, PodanieSocialForm, PodanieKomentarzeForm, SerwerForm, RolaForm, RasaForm

## SERWER
class SerwerListView(ListView):
    template_name = 'rejestracja/serwer_lista.html'
    model = Serwer

class SerwerCreateView(CreateView):
    template_name = 'rejestracja/serwer_create.html'
    model = Serwer
    form_class = SerwerForm
    success_url = reverse_lazy('panel_moda')

class SerwerDeleteView(DeleteView):
    template_name = 'rejestracja/serwer_delete.html'
    model = Serwer
    success_url = reverse_lazy('panel_moda')

## RASA
class RasaListView(ListView):
    template_name = 'rejestracja/rasa_lista.html'
    model = Rasa

class RasaCreateView(CreateView):
    template_name = 'rejestracja/rasa_create.html'
    model = Rasa
    form_class = RasaForm
    success_url = reverse_lazy('panel_moda')

class RasaDeleteView(DeleteView):
    template_name = 'rejestracja/rasa_delete.html'
    model = Rasa
    success_url = reverse_lazy('panel_moda')

## ROLA
class RolaListView(ListView):
    template_name = 'rejestracja/rola_lista.html'
    model = Rola

class RolaCreateView(CreateView):
    template_name = 'rejestracja/rola_create.html'
    model = Rola
    form_class = RolaForm
    success_url = reverse_lazy('panel_moda')

class RolaDeleteView(DeleteView):
    template_name = 'rejestracja/rola_delete.html'
    model = Rola
    success_url = reverse_lazy('panel_moda')

## APLIKACJA
class AplikacjaView(TemplateView):
    template_name = 'rejestracja/aplikacja.html'

class AplikacjaRaidView(CreateView):
    template_name = 'rejestracja/aplikacja_raid.html'
    model = Podanie
    form_class = PodanieRaidForm
    success_url = reverse_lazy('home')

class AplikacjaSocialView(CreateView):
    template_name = 'rejestracja/aplikacja_social.html'
    model = Podanie
    form_class = PodanieSocialForm
    success_url = reverse_lazy('home')

## podanie dla moda
def PodanieDetailView(request, pk):
    context_dict = {}
    try:
        podanie = Podanie.objects.get(pk=pk)
        komentarze = PodanieKomentarze.objects.filter(podanie=podanie)
        context_dict['podanie'] = podanie
        context_dict['komentarze'] = komentarze
    except Podanie.DoesNotExist:
        context_dict['podanie'] = None
        context_dict['komentarze'] = None

    response = render(request, 'rejestracja/podanie_detail.html', context=context_dict)
    return response

def DodajKomentarz(reuqest, pk):
    podanie = Podanie.objects.get(pk=pk)
    komentarze = PodanieKomentarze.objects.filter(podanie=podanie)
    context_dict = {'podanie': podanie, 'komentarze': komentarze}

    response = render(request, 'rejestracja/podanie_komentarz.html', context=context_dict)
    return response

def PanelModaView(request):
    lista_podan = Podanie.objects.order_by('-date')
    list_podan_bez_decyzji = []
    for i in lista_podan:
        if not i.accepted and not i.rejected:
            list_podan_bez_decyzji.append(i)

    context_dict ={'lista': list_podan_bez_decyzji}

    response = render(request, 'panel_moda.html', context=context_dict)
    return response