from django import forms
from django.forms import ModelForm, HiddenInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserProfile, UserPostac
from rejestracja.models import Podanie, Serwer, Rasa, Rola
from pages.models import Klasa

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')
        labels = {'username': '', 'email':''}
        help_texts = {'username': '', 'email': ''}


    def __init__(self, pk, *args, **kwargs):
        podanie = Podanie.objects.get(pk=pk)
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = podanie.name
        self.fields['email'].initial = podanie.email
        self.fields['password1'].required = False
        self.fields['password1'].widget = HiddenInput()
        self.fields['password2'].required = False
        self.fields['password2'].widget = HiddenInput()

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'battleTag',]

    def __init__(self, pk, username, *args, **kwargs):
        podanie = Podanie.objects.get(pk=pk)
        profile_for = CustomUser.objects.get(username=username)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['user'].widget = HiddenInput()
        self.fields['battleTag'].initial = podanie.battleTag

class UserProfileUserForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'picture',]
        labels = {'picture': 'Avatar', 'phone': 'Nr telefonu'}
        help_texts = {'phone': """
        Prosimy o podawanie prawdziwego numeru telefonu. Numer może zostać wykorzystany jedynie w momencie potrzeby kontaktu (np. nie pojawienie się na raidzie).
        Dostęp do numeru ma tylko Guild Master.
        Aby skasować numer pozostaw puste pole i kliknij 'Zapisz' """}
    
    def __init__(self, *args, **kwargs):
        super(UserProfileUserForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False

class UserPostacForm(ModelForm):
    class Meta:
        model = UserPostac
        fields = ['owner', 'name', 'serwer', 'rasa', 'klasa', 'mainspec', 'offspec', 'is_main']
        labels = {'name': 'Nazwa postaci', 'serwer': 'Serwer', 'rasa': 'Rasa', 'klasa': 'Klasa', 'mainspec': 'Main Spec', 'offspec': 'Off Spec'}

    def __init__(self, pk, username, *args, **kwargs):
        podanie = Podanie.objects.get(pk=pk)
        mainspec = podanie.mainspec
        offspec = podanie.offspec
        profile_for = CustomUser.objects.get(username=username)
        super(UserPostacForm, self).__init__(*args, **kwargs)
        self.fields['owner'].required = False
        self.fields['owner'].widget = HiddenInput()
        self.fields['name'].initial = podanie.name
        self.fields['serwer'].queryset = Serwer.objects.filter(podanie=podanie)
        self.fields['rasa'].queryset = Rasa.objects.filter(podanie=podanie)
        self.fields['klasa'].queryset = Klasa.objects.filter(podanie=podanie)
        self.fields['mainspec'].queryset = Rola.objects.filter(mainspec=podanie)
        self.fields['offspec'].queryset = Rola.objects.filter(offspec=podanie)
        self.fields['is_main'].initial = True
        self.fields['is_main'].widget = HiddenInput()

class UserPostacUserForm(ModelForm):
    class Meta:
        model = UserPostac
        fields = ['owner', 'name', 'serwer', 'rasa', 'klasa', 'mainspec', 'offspec', 'is_main']
        labels = {'name': '', 'serwer': '', 'rasa': '', 'klasa': '', 'mainspec': '', 'offspec': ''}

    def __init__(self, username, *args, **kwargs):
        profile_for = CustomUser.objects.get(username=username)
        super(UserPostacUserForm, self).__init__(*args, **kwargs)
        self.fields['owner'].required = False
        self.fields['owner'].widget = HiddenInput()
        self.fields['is_main'].initial = False
        self.fields['is_main'].widget = HiddenInput()


class AplikacjaDoneForm(forms.Form):
    email = forms.CharField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(AplikacjaDoneForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['email'].widget = HiddenInput()

### user tworzy haslo po kliknieciu w link w mailu

class SetPasswordForm(forms.Form):
    error_messages = {'password_mismatch': ("Hasła nie są identyczne!"),}
    new_password1 = forms.CharField(label=("Ustaw hasło"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("Potwórz hasło"), widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch',)
        return password2