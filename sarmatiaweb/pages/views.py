from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from pages.models import Rekrutacja, Klasa
from rejestracja.models import Podanie
from pages.forms import RekrutacjaForm, TworzenieKlasyForm, RekrutacjaNowaForm
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

def HomePageView(request):
    class_list = Klasa.objects.order_by('name')

    context_dict = {'class_list': class_list, }
    response = render(request, 'home.html', context=context_dict)
    return response

@method_decorator(staff_member_required, name='dispatch')
class RekrutacjaListView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    template_name = 'rekrutacja_lista.html'
    model = Rekrutacja

@method_decorator(staff_member_required, name='dispatch')
class RekrutacjaUpdateView(LogoutIfNotStaffMixin, UpdateView):
    login_url = 'login'
    model = Rekrutacja
    template_name = 'rekrutacja_update.html'
    form_class = RekrutacjaForm
    success_url = reverse_lazy('rekrutacja_lista')

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

