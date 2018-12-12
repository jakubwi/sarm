from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
##
from rejestracja.models import Rola
from .models import Wymagania, Event
from .forms import EventCreateForm, WymaganiaUpdateForm, EventUpdateForm, ZapisNaEventForm, ZapisNaEventUpdateForm, ZapisNaEventPonownieForm
from .forms import WyborNaEventFormset
## login required / is_staff /admin
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


class LogoutIfNotStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            logout(request)
            return self.handle_no_permission()
        return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)

def superuser_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                   login_url='account_login_url'):
    """
    Decorator for views that checks that the user is logged in and is a
    superuser, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

@method_decorator(staff_member_required, name='dispatch')
class RpEventCreateView(LogoutIfNotStaffMixin, CreateView):
    login_url = 'login'
    template_name = 'rp/rp_event_create.html'
    model = Event
    form_class = EventCreateForm
    success_url = reverse_lazy('home')

class RpView(LoginRequiredMixin, ListView):
    template_name = 'rp/rp.html'
    login_url = 'login'
    model = Event
    
    def get_queryset(self):
        zapisy = {}
        for event in Event.objects.all():
            if event.status != 3:
                tank = 0
                heal = 0
                dps = 0
                for zapis in event.zapis_set.all():
                    if zapis.czym.mainspec.name == 'Tank':
                        tank += 1
                    elif zapis.czym.mainspec.name == 'Heal':
                        heal += 1
                    else:
                        dps += 1
                suma = tank + heal + dps
                zapisy[event] = [tank, heal, dps, suma]
        queryset = zapisy
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RpView, self).get_context_data(**kwargs)
        context['wymagania'] = Wymagania.objects.all().first()
        return context

class RpHistoriaView(LoginRequiredMixin, ListView):
    template_name = 'rp/rp_historia.html'
    login_url = 'login'
    model = Event

class RpEventDetailView(LoginRequiredMixin, DetailView):
    template_name = 'rp/rp_event_detail.html'
    login_url = 'login'
    model = Event

@login_required(login_url='login')
def RpEventDetailView(request, pk):
    curr_user = request.user
    main = curr_user.userpostac_set.get(is_main=True)
    event = Event.objects.get(pk=pk)
    role = Rola.objects.all()
    new_zapis = None
    zapisani = event.zapis_set.filter(wybrany=False, anulowany=False)
    wybrani = event.zapis_set.filter(wybrany=True, anulowany=False)
    anulowani = event.zapis_set.filter(wybrany=False, anulowany=True)
    user_zapisany = event.zapis_set.filter(kto=curr_user)
    suma = len(event.zapis_set.all())
    suma_bez_anulowanych = suma - len(anulowani)

    user_anulowany = None
    user_wybrany = None
    if len(user_zapisany) >= 1:
        user_zapisany = user_zapisany
        if user_zapisany[0].anulowany:
            user_anulowany = True
        else:
            user_anulowany = False
    else:
        user_zapisany = False
    if user_zapisany != False:
        for user in user_zapisany:
            if user.wybrany:
                user_wybrany = True
            else:
                user_wybrany = False

    if request.method == 'POST':
        if not user_zapisany:
            form = ZapisNaEventForm(request.POST)
        elif user_zapisany and user_anulowany:
            form = ZapisNaEventPonownieForm(request.POST, instance=user_zapisany[0])
        elif user_zapisany:
            form = ZapisNaEventUpdateForm(request.POST, instance=user_zapisany[0])
        if form.is_valid():
            new_zapis = form.save(commit=False)
            new_zapis.na_co = event
            new_zapis.kto = request.user
            new_zapis.czym = main
            new_zapis.save()
            return redirect('rp_event_detail', event.pk)
        else:
            print(form.errors)
    else:                
        if not user_zapisany:
            form = ZapisNaEventForm()
        elif user_zapisany and user_anulowany:
            form = ZapisNaEventPonownieForm(instance=user_zapisany[0])
        elif user_zapisany:
            form = ZapisNaEventUpdateForm(instance=user_zapisany[0])
        elif user_zapisany and user_wybrany:
            form = None
        context_dict = {'event': event,
                        'new_zapis': new_zapis,
                        'form': form,
                        'zapisani': zapisani,
                        'wybrani': wybrani,
                        'anulowani': anulowani,
                        'role': role,
                        'main': main,
                        'user_zapisany': user_zapisany,
                        'user_anulowany': user_anulowany,
                        'user_wybrany': user_wybrany,
                        'suma': suma,
                        'suma_bez_anulowanych': suma_bez_anulowanych,}
        response = render(request, 'rp/rp_event_detail.html', context=context_dict)
        return response

@staff_member_required(login_url='login')
def RpEventWybierzSkladView(request, pk):
    event = Event.objects.get(pk=pk)
    zapisani = event.zapis_set.filter(anulowany=False)
    anulowani = event.zapis_set.filter(wybrany=False, anulowany=True)
    tanki = event.zapis_set.filter(czym__mainspec__name__startswith='Tank', anulowany=False, wybrany=False)
    healerzy = event.zapis_set.filter(czym__mainspec__name__startswith='Heal', anulowany=False, wybrany=False)
    ranged = event.zapis_set.filter(czym__mainspec__name__startswith='Ranged', anulowany=False, wybrany=False)
    melee = event.zapis_set.filter(czym__mainspec__name__startswith='Melee', anulowany=False, wybrany=False)
    tankiWybrani = event.zapis_set.filter(czym__mainspec__name__startswith='Tank', anulowany=False, wybrany=True)
    healerzyWybrani = event.zapis_set.filter(czym__mainspec__name__startswith='Heal', anulowany=False, wybrany=True)
    rangedWybrani = event.zapis_set.filter(czym__mainspec__name__startswith='Ranged', anulowany=False, wybrany=True)
    meleeWybrani = event.zapis_set.filter(czym__mainspec__name__startswith='Melee', anulowany=False, wybrany=True)
    suma = len(event.zapis_set.all())
    suma_bez_anulowanych = suma - len(anulowani)

    if request.method == 'POST':
        formsetTank = WyborNaEventFormset(request.POST, instance=event, queryset=tanki, prefix='Tank')
        formsetHeal = WyborNaEventFormset(request.POST, instance=event, queryset=healerzy, prefix='Heal')
        formsetRanged = WyborNaEventFormset(request.POST, instance=event, queryset=ranged, prefix='Ranged')
        formsetMelee = WyborNaEventFormset(request.POST, instance=event, queryset=melee, prefix='Melee')
        formsetTankWybrani = WyborNaEventFormset(request.POST, instance=event, queryset=tankiWybrani, prefix='TankWybrani')
        formsetHealWybrani = WyborNaEventFormset(request.POST, instance=event, queryset=healerzyWybrani, prefix='HealWybrani')
        formsetRangedWybrani = WyborNaEventFormset(request.POST, instance=event, queryset=rangedWybrani, prefix='RangedWybrani')
        formsetMeleeWybrani = WyborNaEventFormset(request.POST, instance=event, queryset=meleeWybrani, prefix='MeleeWybrani')
        if formsetTank.is_valid() and formsetHeal.is_valid() and formsetRanged.is_valid() and formsetMelee.is_valid() and formsetTankWybrani.is_valid() and formsetHealWybrani.is_valid() and formsetRangedWybrani.is_valid() and formsetMeleeWybrani.is_valid():
            formsetTank.save()
            formsetHeal.save()
            formsetRanged.save()
            formsetMelee.save()
            formsetTankWybrani.save()
            formsetHealWybrani.save()
            formsetRangedWybrani.save()
            formsetMeleeWybrani.save()
            return redirect('rp_event_detail', event.pk)

    else:
        formsetTank = WyborNaEventFormset(instance=event, queryset=tanki, prefix='Tank')
        formsetHeal = WyborNaEventFormset(instance=event, queryset=healerzy, prefix='Heal')
        formsetRanged = WyborNaEventFormset(instance=event, queryset=ranged, prefix='Ranged')
        formsetMelee = WyborNaEventFormset(instance=event, queryset=melee, prefix='Melee')
        formsetTankWybrani = WyborNaEventFormset(instance=event, queryset=tankiWybrani, prefix='TankWybrani')
        formsetHealWybrani = WyborNaEventFormset(instance=event, queryset=healerzyWybrani, prefix='HealWybrani')
        formsetRangedWybrani = WyborNaEventFormset(instance=event, queryset=rangedWybrani, prefix='RangedWybrani')
        formsetMeleeWybrani = WyborNaEventFormset(instance=event, queryset=meleeWybrani, prefix='MeleeWybrani')
    context_dict = {'event': event,
                        'zapisani': zapisani,
                        'anulowani': anulowani,
                        'suma': suma,
                        'suma_bez_anulowanych': suma_bez_anulowanych,
                        'formsetTank': formsetTank,
                        'formsetHeal': formsetHeal,
                        'formsetRanged': formsetRanged,
                        'formsetMelee': formsetMelee,
                        'formsetTankWybrani': formsetTankWybrani,
                        'formsetHealWybrani': formsetHealWybrani,
                        'formsetRangedWybrani': formsetRangedWybrani,
                        'formsetMeleeWybrani': formsetMeleeWybrani,
                        'tanki': tanki,
                        'healerzy': healerzy,
                        'ranged': ranged,
                        'melee': melee,
                        'tankiWybrani': tankiWybrani,
                        'healerzyWybrani': healerzyWybrani,
                        'rangedWybrani': rangedWybrani,
                        'meleeWybrani': meleeWybrani,}
    response = render(request, 'rp/rp_event_wybierz.html', context=context_dict)
    return response

@method_decorator(staff_member_required, name='dispatch')
class RpEventUpdateView(LogoutIfNotStaffMixin, UpdateView):
    login_url = 'login'
    model = Event
    template_name = 'rp/rp_event_update.html'
    success_url = reverse_lazy('rp')
    form_class = EventUpdateForm
    
@method_decorator(staff_member_required, name='dispatch')
class RpWymaganiaUpdate(LogoutIfNotStaffMixin, UpdateView):
    login_url = 'login'
    model = Wymagania
    template_name = 'rp/rp_wymagania.html'
    success_url = reverse_lazy('rp')
    form_class = WymaganiaUpdateForm

    def get_context_data(self, **kwargs):
        context = super(RpWymaganiaUpdate, self).get_context_data(**kwargs)
        context['wymaganie'] = Wymagania.objects.all().first()
        return context
        