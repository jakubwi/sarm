from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib import messages
##
from rejestracja.models import Rola
from .models import Wymagania, Event, EventBlueprint, Zapis
from .forms import EventCreateForm, WymaganiaUpdateForm, EventUpdateForm, ZapisNaEventForm
from .forms import ZapisNaEventAltForm, ZapisNaEventPonownieAltForm, ZapisNaEventUpdateAltForm
from .forms import ZapisNaEventUpdateForm, ZapisNaEventPonownieForm, EventBlueprintCreateForm, EventCreateFromBlueprintForm
from .forms import WyborNaEventFormset, EventCreateFromBlueprintFormset
## login required / is_staff /admin
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
## pagination 
from pure_pagination.mixins import PaginationMixin


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

@staff_member_required(login_url='login')
def RpEventNewView(request):
    szablony = EventBlueprint.objects.all()
    context_dict =  {'szablony': szablony}
    return render(request, 'rp/rp_event_new.html', context=context_dict)

@staff_member_required(login_url='login')
def RpEventCreateFromBlueprintView(request, pk):
    szablon = EventBlueprint.objects.get(pk=pk)
    data = [{'nazwa': szablon.nazwaEventu, 
            'kiedy_godzina': szablon.kiedy_godzina, 
            'opis': szablon.opis,
            'miejsca': szablon.miejsca,
            'alty': szablon.alty},]
    formset = EventCreateFromBlueprintFormset(form_kwargs={'szablon': szablon},)

    if request.method == 'POST':
        formset = EventCreateFromBlueprintFormset(request.POST, form_kwargs={'szablon': szablon},)
        for form in formset:
            if form.is_valid:
                form.save()
        return redirect('rp')

    else:
        formset = EventCreateFromBlueprintFormset(form_kwargs={'szablon': szablon},)

    context_dict =  {'szablon': szablon,
                    'formset': formset}
    return render(request, 'rp/rp_event_create_from_blueprint.html', context=context_dict)

@method_decorator(staff_member_required, name='dispatch')
class RpEventBlueprintCreateView(LogoutIfNotStaffMixin, CreateView):
    login_url = 'login'
    template_name = 'rp/rp_event_blueprint_create.html'
    model = EventBlueprint
    form_class = EventBlueprintCreateForm
    success_url = reverse_lazy('rp')

@login_required(login_url='login')
def RpView(request):
    events = Event.objects.all()
    wymagania = Wymagania.objects.all().first()
    curr_user = request.user
    main = curr_user.userpostac_set.get(is_main=True)
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
    
    if request.method == 'POST':
        multizapis = request.POST.getlist('multizapis') 
        for zapis_id in multizapis:
            try:
                event = Event.objects.get(id=(int(zapis_id)))
                czyZapisano = event.zapis_set.get(kto=curr_user)
                messages.error(request, 'Jesteś już zapisany na: ' + str(event))
            except Zapis.DoesNotExist:
                z = Zapis()
                z.kto = curr_user
                z.czym = main
                z.na_co = Event.objects.get(id=int(zapis_id))
                z.save()           
                messages.success(request, 'Zapisano na: ' + str(event))
        return redirect('rp')
    else:                
        
        context_dict = {'wymagania': wymagania,
                        'zapisy': zapisy,
                        'events': events,
                        'curr_user': curr_user,}
        response = render(request, 'rp/rp.html', context=context_dict)
        return response

class RpHistoriaView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'rp/rp_historia.html'
    login_url = 'login'
    model = Event
    paginate_by = 25
    ordering = ['-kiedy_dzien', '-kiedy_godzina',]

@login_required(login_url='login')
def RpEventDetailView(request, pk):
    curr_user = request.user
    main = curr_user.userpostac_set.get(is_main=True)
    postacie = curr_user.userpostac_set.all()
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
            if event.alty:
                form = ZapisNaEventAltForm(postacie, request.POST)
            elif not event.alty:
                form = ZapisNaEventForm(request.POST)
        elif user_zapisany and user_anulowany:
            if event.alty:
                form = ZapisNaEventPonownieAltForm(postacie, request.POST, instance=user_zapisany[0])
            elif not event.alty:
                form = ZapisNaEventPonownieForm(request.POST, instance=user_zapisany[0])
        elif user_zapisany:
            if event.alty:
                form = ZapisNaEventUpdateAltForm(postacie, request.POST, instance=user_zapisany[0])
            elif not event.alty:
                form = ZapisNaEventUpdateForm(request.POST, instance=user_zapisany[0])
        if form.is_valid() and not event.alty:
            new_zapis = form.save(commit=False)
            new_zapis.na_co = event
            new_zapis.kto = request.user
            new_zapis.czym = main
            new_zapis.save()
            return redirect('rp_event_detail', event.pk)
        elif form.is_valid() and event.alty:
            new_zapis = form.save(commit=False)
            new_zapis.na_co = event
            new_zapis.kto = request.user
            new_zapis.save()
            return redirect('rp_event_detail', event.pk)
        else:
            print(form.errors)
    else:                
        if not user_zapisany:
            if event.alty:
                form = ZapisNaEventAltForm(postacie)
            elif not event.alty:
                form = ZapisNaEventForm()
        elif user_zapisany and user_anulowany:
            if event.alty:
                form = ZapisNaEventPonownieAltForm(postacie, instance=user_zapisany[0])
            elif not event.alty:
                form = ZapisNaEventPonownieForm(instance=user_zapisany[0])
        elif user_zapisany:
            if event.alty:
                form = ZapisNaEventUpdateAltForm(postacie, instance=user_zapisany[0])
            elif not event.alty:
                form = ZapisNaEventUpdateForm(instance=user_zapisany[0])

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
                        'suma_bez_anulowanych': suma_bez_anulowanych,
                        'postacie': postacie,}
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
        
