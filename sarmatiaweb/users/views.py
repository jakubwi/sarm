from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import AbstractUser, User
from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.views.generic import CreateView, FormView
from django.views.generic.edit import UpdateView
from .forms import CustomUserCreationForm, UserProfileForm, SetPasswordForm, UserPostacForm, UserProfileUserForm, UserPostacUserForm
from .models import UserProfile, UserPostac, CustomUser
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


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

### tworzenie nowego hasla z maila po akceptacji podania
class NoweHasloView(FormView):
    template_name = "registration/password_reset_confirm_mod.html"
    form_class = SetPasswordForm
    success_url = 'panel'

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        UserModel = settings.AUTH_USER_MODEL
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None
    
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Utworzono nowe hasło!')
                return self.form_valid(form)
            else:
                messages.error(request, 'Wystąpił błąd.')
                return self.form_invalid(form)
        else:
            messages.error(request,'Link do tworzenia nowego hasła wygasł. Skontaktuj się z Gild Masterem w grze.')
            return self.form_invalid(form)

@login_required(login_url='login')
def ProfilView(request):
    user = request.user
    postacie = UserPostac.objects.filter(owner=user)
    userprofile = UserProfile.objects.get_or_create(user=user) [0]
    form = UserProfileUserForm()
    ilosc_postaci = len(postacie)
    main = None
    for postac in postacie:
        if postac.is_main:
            main = postac

    if request.method == 'POST':
        form = UserProfileUserForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profil')
        else:
            print(form.errors)
    
    return render(request, 'profil.html', {'userprofile': userprofile, 'user': user, 'form': form, 'postacie':postacie, 'ilosc_postaci': ilosc_postaci, 'main':main})

@login_required(login_url='login')
def ProfilDodajPostacView(request, username):
    username=username
    profile_for = CustomUser.objects.get(username=username)
    new_postac = None

    if request.method == 'POST':
        form = UserPostacUserForm(username, request.POST)
        if form.is_valid():
            new_postac = form.save(commit=False)
            new_postac.owner = profile_for
            new_postac.save()
            return redirect('profil')
        else:
            print(form.errors)

    else:
        form = UserPostacUserForm(username)

    context_dict = {    'username': username, 
                        'profile_for': profile_for,
                        'new_postac': new_postac,
                        'form': form,}
    response = render(request, 'profil_dodaj_postac.html', context=context_dict)
    return response