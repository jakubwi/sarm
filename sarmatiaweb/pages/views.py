from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from pages.models import Rekrutacja, Klasa, Killshot
from rejestracja.models import Podanie
from pages.forms import TworzenieKlasyForm, RekrutacjaNowaForm, KillshotCreateForm, RekrutacjaForm, RekrutacjaFormSet
from progress.models import Boss, Raid, Expansion
## login required / is_staff /admin
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Count

class LogoutIfNotStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            logout(request)
            return self.handle_no_permission()
        return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)


class HomePageView(ListView):   
    template_name = 'home.html'

    def get_queryset(self):
        try:
            aktualny_dodatek = Expansion.objects.all().order_by('-position')[0]
            poprzedni_dodatek = Expansion.objects.all().order_by('-position')[1]
        except IndexError:
            queryset = None
            return queryset
        if aktualny_dodatek.raids.all().count() <= 1:
            poprzednie_raidy = {}
            for raid in poprzedni_dodatek.raids.all():
                mythic = 0
                heroic = 0
                normal = 0
                for boss in raid.bosses.all():
                    if boss.mythic:
                        mythic += 1
                    if boss.heroic:
                        heroic += 1
                    if boss.normal:
                        normal += 1
                if mythic >= 1:
                    poprzednie_raidy[raid.name] = ['Mythic', mythic, raid.bosses.all().count()]
                elif heroic >= 1:
                    poprzednie_raidy[raid.name] = ['Heroic', heroic, raid.bosses.all().count()]
                elif normal >= 1:
                    poprzednie_raidy[raid.name] = ['Normal', normal, raid.bosses.all().count()]
                else:
                    poprzednie_raidy[raid.name] = ['Nie', 0, raid.bosses.all().count()]
            queryset = poprzednie_raidy
            return queryset
        elif aktualny_dodatek.raids.all().count()  > 1:
            aktualne_raidy = {}
            for raid in aktualny_dodatek.raids.all():
                mythic = 0
                heroic = 0
                normal = 0
                for boss in raid.bosses.all():
                    if boss.mythic:
                        mythic += 1
                    if boss.heroic:
                        heroic += 1
                    if boss.normal:
                        normal += 1
                if mythic >= 1:
                    aktualne_raidy[raid.name] = ['Mythic', mythic, raid.bosses.all().count()]
                elif heroic >= 1:
                    aktualne_raidy[raid.name] = ['Heroic', heroic, raid.bosses.all().count()]
                elif normal >= 1:
                    aktualne_raidy[raid.name] = ['Normal', normal, raid.bosses.all().count()]
                else:
                    aktualne_raidy[raid.name] = ['Nie', 0, raid.bosses.all().count()]
            queryset = aktualne_raidy
            return queryset
        else:
            pass

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['class_list'] = Klasa.objects.order_by('name')
        context['killshots_list'] = Killshot.objects.order_by('date')
        context['first_shot'] = Killshot.objects.all().first()
        try:
            context['aktualny_dodatek'] = Expansion.objects.all().order_by('-position')[0]
            context['poprzedni_dodatek'] = Expansion.objects.all().order_by('-position')[1]
        except IndexError:
            context['aktualny_dodatek'] = None
            context['poprzedni_dodatek'] = None
        return context

### dodaj/usun killshot
@method_decorator(staff_member_required, name='dispatch')
class KillshotCreateView(LogoutIfNotStaffMixin, CreateView):
    login_url = 'login'
    template_name = 'killshots/killshot_create.html'
    model = Killshot
    form_class = KillshotCreateForm
    success_url = reverse_lazy('panel_moda')

@method_decorator(staff_member_required, name='dispatch')
class KillshotListView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    template_name = 'killshots/killshot_lista.html'
    model = Killshot
    
@method_decorator(staff_member_required, name='dispatch')
class KillshotDeleteView(LogoutIfNotStaffMixin, DeleteView):
    login_url = 'login'
    template_name = 'killshots/killshot_delete.html'
    model = Killshot
    success_url = reverse_lazy('panel_moda')

## REKRUTACJA    
@staff_member_required
def RekrutacjaUpdateView(request):
    rekrutacja_list = Rekrutacja.objects.all()
    klasa = Klasa
    ilosc_klas = len(Klasa.objects.all())
    
    if request.method == 'POST':
        formset = RekrutacjaFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('home')
        else:
            print(formset.errors)
    else:
        formset = RekrutacjaFormSet()
    context_dict = {'formset': formset,
                    'rekrutacja_list': rekrutacja_list,
                    'ilosc_klas': ilosc_klas,
                    'klasa': klasa,}
    response = render(request, 'rekrutacja_update.html', context=context_dict)
    return response

@method_decorator(staff_member_required, name='dispatch')
class KlasaCreateView(LogoutIfNotStaffMixin, CreateView):
    login_url = 'login'
    template_name = 'rejestracja/klasa_create.html'
    model = Klasa
    form_class = TworzenieKlasyForm
    
    def get_success_url(self):
        return reverse('rekrutacja_create', args=(self.object.pk,))

@method_decorator(staff_member_required, name='dispatch')
class RekrutacjaCreateView(LogoutIfNotStaffMixin, CreateView):
    login_url = 'login'
    template_name = 'rekrutacja_create.html'
    model = Rekrutacja
    form_class = RekrutacjaNowaForm
    success_url = reverse_lazy('home')

@method_decorator(staff_member_required, name='dispatch')
class KlasaListView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    model = Klasa
    template_name = 'rejestracja/klasa_lista.html'

@method_decorator(staff_member_required, name='dispatch')
class KlasaDeleteView(LogoutIfNotStaffMixin, DeleteView):
    login_url = 'login'
    template_name = 'rejestracja/klasa_delete.html'
    model = Klasa
    success_url = reverse_lazy('panel_moda')

