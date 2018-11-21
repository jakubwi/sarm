from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy, reverse
## for sending email
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.conf import settings
from django.db.models.query_utils import Q
from django.core.mail import send_mail
#
from django.contrib.auth.models import AbstractUser, User
from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from rejestracja.models import Serwer, Rasa, Rola, Podanie, PodanieKomentarze
from rejestracja.forms import PodanieRaidForm, PodanieSocialForm, PodanieKomentarzeForm, SerwerForm, RolaForm, RasaForm
from users.models import CustomUser, UserProfile
from users.forms import CustomUserCreationForm, UserProfileForm, UserPostacForm, AplikacjaDoneForm
## login required / is_staff /admin
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
## django-filter
from .filters import AplikacjeZamknieteFilter
from django.db.models import Q
from django.db.models import Count
## pagination 

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger




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

## SERWER
@method_decorator(staff_member_required, name='dispatch')
class SerwerListView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    template_name = 'rejestracja/serwer_lista.html'
    model = Serwer

@method_decorator(staff_member_required, name='dispatch')
class SerwerCreateView(LogoutIfNotStaffMixin, CreateView):
    login_url = 'login'
    template_name = 'rejestracja/serwer_create.html'
    model = Serwer
    form_class = SerwerForm
    success_url = reverse_lazy('panel_moda')

@method_decorator(staff_member_required, name='dispatch')
class SerwerDeleteView(LogoutIfNotStaffMixin, DeleteView):
    login_url = 'login'
    template_name = 'rejestracja/serwer_delete.html'
    model = Serwer
    success_url = reverse_lazy('panel_moda')

## RASA
@method_decorator(staff_member_required, name='dispatch')
class RasaListView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    template_name = 'rejestracja/rasa_lista.html'
    model = Rasa

@method_decorator(staff_member_required, name='dispatch')
class RasaCreateView(LogoutIfNotStaffMixin, CreateView):
    login_url = 'login'
    template_name = 'rejestracja/rasa_create.html'
    model = Rasa
    form_class = RasaForm
    success_url = reverse_lazy('panel_moda')

@method_decorator(staff_member_required, name='dispatch')
class RasaDeleteView(LogoutIfNotStaffMixin, DeleteView):
    login_url = 'login'
    template_name = 'rejestracja/rasa_delete.html'
    model = Rasa
    success_url = reverse_lazy('panel_moda')

## ROLA
@method_decorator(staff_member_required, name='dispatch')
class RolaListView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    template_name = 'rejestracja/rola_lista.html'
    model = Rola

@method_decorator(staff_member_required, name='dispatch')
class RolaCreateView(LogoutIfNotStaffMixin, CreateView):
    login_url = 'login'
    template_name = 'rejestracja/rola_create.html'
    model = Rola
    form_class = RolaForm
    success_url = reverse_lazy('panel_moda')

@method_decorator(staff_member_required, name='dispatch')
class RolaDeleteView(LogoutIfNotStaffMixin, DeleteView):
    login_url = 'login'
    template_name = 'rejestracja/rola_delete.html'
    model = Rola
    success_url = reverse_lazy('panel_moda')

## SKŁADANIE APLIKACJI 
class AplikacjaView(TemplateView):
    template_name = 'aplikacje/aplikacja.html'

class AplikacjaRaidView(CreateView):
    template_name = 'aplikacje/aplikacja_raid.html'
    model = Podanie
    form_class = PodanieRaidForm
    success_url = reverse_lazy('home')

class AplikacjaSocialView(CreateView):
    template_name = 'aplikacje/aplikacja_social.html'
    model = Podanie
    form_class = PodanieSocialForm
    success_url = reverse_lazy('home')

## dodawanie moderatora / usuwanie moderatora
@method_decorator(superuser_required(login_url='login'), name='dispatch', )
class ModWybierzView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    model = CustomUser
    template_name = 'rejestracja/mod_wybierz.html'

@method_decorator(superuser_required(login_url='login'), name='dispatch')
class ModChangeView(LogoutIfNotStaffMixin, UpdateView):
    login_url = 'login'
    model = CustomUser
    template_name = 'rejestracja/mod_create.html'
    success_url = reverse_lazy('panel_moda')
    fields = ['is_staff']

@method_decorator(superuser_required(login_url='login'), name='dispatch')
class ModListView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    model = CustomUser
    template_name = 'rejestracja/mod_lista.html'


### panel moda
@staff_member_required
def PanelModaView(request):
    lista_podan = Podanie.objects.all()
    list_podan_bez_decyzji = []
    for i in lista_podan:
        if not i.accepted and not i.rejected:
            list_podan_bez_decyzji.append(i)

    context_dict ={'lista': list_podan_bez_decyzji}

    response = render(request, 'panel_moda.html', context=context_dict)
    return response

## zaakceptowane i odrzucone podania
@staff_member_required
def AplikacjeZamkniete(request):
    data = request.GET.copy()
    if 'page' in data:
        del data['page']
    f = AplikacjeZamknieteFilter(data, queryset=Podanie.objects.filter(Q(accepted=True) | Q(rejected=True)))
    c = Podanie.objects.annotate(num_comm=Count('comments')).filter(num_comm__gte=1)

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(f.qs, request=request, per_page=7)
    appli = p.page(page)

    context_dict = {'filter': f, 
                    'c': c,
                    'appli': appli,}
    
    return render(request, 'aplikacje/aplikacje_closed.html', context=context_dict)

## podanie
@staff_member_required
def AplikacjaDetailView(request, pk):
    podanie = Podanie.objects.get(pk=pk)
    comment_list = podanie.comments.filter(podanie=podanie)
    authors = UserProfile.objects.all()
    new_comment = None

    if request.method == 'POST':
        form = PodanieKomentarzeForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.podanie = podanie
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Komentarz dodany.')
            return redirect('aplikacja_detail', podanie.pk)
        else:
            print(form.errors)
            messages.error(request, 'Błąd. Komentarz nie został dodany.')

    else:
        form = PodanieKomentarzeForm()
        context_dict = {'podanie': podanie, 
                        'comment_list': comment_list, 
                        'new_comment': new_comment,
                        'form': form,
                        'authors': authors}
        response = render(request, 'aplikacje/aplikacja_detail.html', context=context_dict)
        return response

@staff_member_required
def AplikacjaDeleteKomentarz(request, pk, kpk):

    koment = PodanieKomentarze.objects.get(pk=kpk)

    if request.method == "POST" and request.user == koment.author:
        koment.delete()
        return redirect('aplikacja_detail', pk=pk)
    
    context= {'koment': koment, 'pk':pk}
    
    return render(request, 'aplikacje/aplikacja_delete_komentarz.html', context)

### AKCEPTACJA PODANIA
@staff_member_required
def AplikacjaConfirm(request, pk):
    podanie = Podanie.objects.get(pk=pk)
    new_user = None
    username = None
    if request.method == 'POST':
        form = CustomUserCreationForm(pk, request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = new_user.username
            new_user.save()
            return redirect('aplikacja_confirm2', podanie.pk, username)
        else:
            print(form.errors)
            
    else:
        form = CustomUserCreationForm(pk)
    context_dict = {'podanie': podanie, 
                        'new_user': new_user,
                        'username': username,
                        'form': form,}
    response = render(request, 'aplikacje/aplikacja_confirm.html', context=context_dict)
    return response

@staff_member_required
def AplikacjaConfirm2(request, pk, username):
    podanie = Podanie.objects.get(pk=pk)
    username=username
    profile_for = CustomUser.objects.get(username=username)
    new_profile = None

    if request.method == 'POST':
        form = UserProfileForm(pk, username, request.POST)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = profile_for
            new_profile.save()
            return redirect('aplikacja_confirm3', podanie.pk, username)
        else:
            print(form.errors)

    else:
        form = UserProfileForm(pk, username)
    context_dict = {'podanie': podanie,
                        'username': username, 
                        'profile_for': profile_for,
                        'new_profile': new_profile,
                        'form': form,}
    response = render(request, 'aplikacje/aplikacja_confirm2.html', context=context_dict)
    return response

@staff_member_required
def AplikacjaConfirm3(request, pk, username):
    podanie = Podanie.objects.get(pk=pk)
    username=username
    profile_for = CustomUser.objects.get(username=username)
    new_postac = None
    aplikacja_done = None

    if request.method == 'POST':
        form = UserPostacForm(pk, username, request.POST)
        form2 = AplikacjaDoneForm(request.POST)
        if form.is_valid() and form2.is_valid():
            new_postac = form.save(commit=False)
            new_postac.owner = profile_for
            ## sending email
            c = {'email': profile_for.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'Sarmatia WoW',
                'uid': urlsafe_base64_encode(force_bytes(profile_for.pk)).decode(),
                'user': profile_for,
                'token': default_token_generator.make_token(profile_for),
                'protocol': 'http',}
            subject_template_name='registration/password_reset_subject_mod.txt' 
            email_template_name='registration/password_reset_email_mod.html'    
            subject = loader.render_to_string(subject_template_name, c)
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [profile_for.email], fail_silently=False)
            ## email sent
            podanie.accepted = True
            podanie.save()
            new_postac.save()
            return redirect('aplikacja_confirm4')
        else:
            print(form.errors)

    else:
        form = UserPostacForm(pk, username)
        form2 = AplikacjaDoneForm()
    context_dict = {'podanie': podanie,
                        'username': username, 
                        'profile_for': profile_for,
                        'new_postac': new_postac,
                        'aplikacja_done': aplikacja_done,
                        'form': form,
                        'form2': form2}
    response = render(request, 'aplikacje/aplikacja_confirm3.html', context=context_dict)
    return response

@method_decorator(staff_member_required, name='dispatch')
class AplikacjaConfirm4(LogoutIfNotStaffMixin, TemplateView):
    login_url = 'login'
    template_name = 'aplikacje/aplikacja_confirm4.html'

## ODRZUCENIE PODANIA

@staff_member_required
def AplikacjaReject(request, pk):
    podanie = Podanie.objects.get(pk=pk)
    podanie_email = podanie.email

    if request.method == 'POST':
        send_mail('Sarmatia - Aplikacja Odrzucona', 
                    'Przykro nam, Twoje podanie do gildii zostało odrzucone.', 
                    settings.DEFAULT_FROM_EMAIL, 
                    [podanie_email], 
                    fail_silently=False, )
        podanie.rejected = True
        podanie.save()
        return redirect('aplikacje_zamkniete')

    context_dict = {'podanie': podanie,
                        'podanie_email': podanie_email,}
    response = render(request, 'aplikacje/aplikacja_reject.html', context=context_dict)
    return response
