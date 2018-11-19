from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from pages.models import Rekrutacja, Klasa, Killshot
from rejestracja.models import Podanie
from pages.forms import TworzenieKlasyForm, RekrutacjaNowaForm, KillshotCreateForm, RekrutacjaForm, RekrutacjaFormSet
## login required / is_staff /admin
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

class LogoutIfNotStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            logout(request)
            return self.handle_no_permission()
        return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)


class HomePageView(ListView):
    context_object_name = 'class_list'    
    template_name = 'home.html'
    queryset = Klasa.objects.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['killshots_list'] = Killshot.objects.order_by('date')
        context['first_shot'] = Killshot.objects.all().first()
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

