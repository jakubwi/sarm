from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Expansion, Boss, Raid
## update forms
from .forms import BossUpdateForm, RaidUpdateForm, ExpansionUpdateForm, RaidUpdateFormset
## create forms
from .forms import ExpansionCreateForm, RaidCreateForm
## login required / is_staff /admin
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
## inne
from django.db.models import Count


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
class ProgressView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    model = Expansion   
    template_name = 'progress/progress.html'

    def get_context_data(self, **kwargs):
        context = super(ProgressView, self).get_context_data(**kwargs)
        context['expansion_list'] = Expansion.objects.all()
        try:
            context['aktualny_dodatek'] = Expansion.objects.all().order_by('-position')[0]
            context['poprzedni_dodatek'] = Expansion.objects.all().order_by('-position')[1]
        except IndexError:
            context['aktualny_dodatek'] = None
            context['poprzedni_dodatek'] = None
        return context

## EXPANSION
@method_decorator(staff_member_required, name='dispatch')
class ExpansionUpdateView(LogoutIfNotStaffMixin, UpdateView):
    login_url = 'login'
    model = Expansion
    template_name = 'progress/progress_expansion_update.html'
    success_url = reverse_lazy('progress')
    form_class = ExpansionUpdateForm

@method_decorator(staff_member_required, name='dispatch')
class ExpansionCreateView(LogoutIfNotStaffMixin, CreateView):
    template_name = 'progress/progress_expansion_create.html'
    model = Expansion
    form_class = ExpansionCreateForm
    success_url = reverse_lazy('progress')

## RAID
@staff_member_required
def RaidUpdateInlineView(request, pk):
    raid = Raid.objects.get(pk=pk)
    form = RaidUpdateForm
    formset = RaidUpdateFormset
    if request.method == "POST":
        form = RaidUpdateForm(request.POST, instance=raid)
        formset = RaidUpdateFormset(request.POST, instance=raid)
        if formset.is_valid() and form.is_valid():
            formset.save()
            form.save()
            return redirect('progress')
    else:
        form = RaidUpdateForm(instance=raid)
        formset = RaidUpdateFormset(instance=raid)
    return render(request, 'progress/progress_raid_update.html', {'formset': formset, 'raid': raid, 'form':form})

@method_decorator(staff_member_required, name='dispatch')
class RaidCreateView(LogoutIfNotStaffMixin, CreateView):
    template_name = 'progress/progress_raid_create.html'
    model = Raid
    form_class = RaidCreateForm
    success_url = reverse_lazy('progress')

@method_decorator(staff_member_required, name='dispatch')
class RaidDeleteView(LogoutIfNotStaffMixin, DeleteView):
    login_url = 'login'
    template_name = 'progress/progress_raid_delete.html'
    model = Raid
    success_url = reverse_lazy('progress')

## BOSS
""" @method_decorator(superuser_required(login_url='login'), name='dispatch', )
class ModWybierzView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    model = CustomUser
    template_name = 'rejestracja/mod_wybierz.html' """

@method_decorator(staff_member_required, name='dispatch')
class BossUpdateView(LogoutIfNotStaffMixin, UpdateView):
    login_url = 'login'
    model = Boss
    template_name = 'progress/progress_boss_update.html'
    success_url = reverse_lazy('home')
    form_class = BossUpdateForm

""" @method_decorator(superuser_required(login_url='login'), name='dispatch')
class ModListView(LogoutIfNotStaffMixin, ListView):
    login_url = 'login'
    model = CustomUser
    template_name = 'rejestracja/mod_lista.html' """

