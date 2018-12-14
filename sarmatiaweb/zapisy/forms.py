from django.forms import ModelForm, forms, modelformset_factory, HiddenInput, inlineformset_factory, formset_factory
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import SelectDateWidget
from .models import Wymagania, Event, Zapis, EventBlueprint
from users.models import CustomUser
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from datetime import datetime

### create forms
class EventCreateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['nazwa', 'kiedy_dzien', 'kiedy_godzina', 'opis', 'miejsca', 'alty']
        labels = {'nazwa': 'Nazwa Eventu', 
                    'kiedy_dzien': 'Wybierz dzień', 
                    'kiedy_godzina': 'Wybierz godzinę', 
                    'opis': 'Dodatkowe info', 
                    'miejsca': 'Ilość miejsc',
                    'alty': 'Zapisy dla również dla Altów'}
        widgets = {'kiedy_dzien': DatePickerInput(format='%Y-%m-%d'),
                    'kiedy_godzina': TimePickerInput(format='%H:%M:%S'),}

class EventCreateFromBlueprintForm(ModelForm):
    class Meta:
        model = Event
        fields = ['nazwa', 'kiedy_dzien', 'kiedy_godzina', 'opis', 'miejsca', 'alty']
        labels = {'kiedy_dzien': '',}
        widgets = {'kiedy_dzien': SelectDateWidget(),
                    'kiedy_godzina': TimePickerInput(format='%H:%M:%S'),}

    def __init__(self, *args, szablon, **kwargs):
        szablon = szablon
        super(EventCreateFromBlueprintForm, self).__init__(*args, **kwargs)
        self.fields['nazwa'].initial = szablon.nazwaEventu
        self.fields['nazwa'].widget = HiddenInput()
        self.fields['kiedy_dzien'].initial = datetime.now
        self.fields['kiedy_godzina'].initial = szablon.kiedy_godzina
        self.fields['kiedy_godzina'].widget = HiddenInput()
        self.fields['opis'].initial = szablon.opis
        self.fields['opis'].widget = HiddenInput()
        self.fields['miejsca'].initial = szablon.miejsca
        self.fields['miejsca'].widget = HiddenInput()
        self.fields['alty'].initial = szablon.alty
        self.fields['alty'].widget = HiddenInput()

EventCreateFromBlueprintFormset = formset_factory(form=EventCreateFromBlueprintForm, extra=1, can_delete=False)
                    
class EventBlueprintCreateForm(ModelForm):
    class Meta:
        model = EventBlueprint
        fields = ['nazwaSzablonu', 'nazwaEventu', 'kiedy_godzina', 'opis', 'miejsca', 'alty']
        widgets = {'kiedy_godzina': TimePickerInput(format='%H:%M:%S'),}

class EventUpdateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['nazwa', 'kiedy_dzien', 'kiedy_godzina', 'opis', 'miejsca', 'alty', 'odblokuj_zapisy', 'usuniety']
        widgets = {'kiedy_dzien': DatePickerInput(format='%Y-%m-%d'),
                    'kiedy_godzina': TimePickerInput(format='%H:%M:%S'),}

class WymaganiaUpdateForm(ModelForm):
    class Meta:
        model = Wymagania
        fields = ['text',]
        labels = {'text': '',}

class ZapisNaEventForm(ModelForm):
    class Meta:
        model = Zapis
        fields = ['kto', 'gotowosc', 'komentarz',]
        labels = {'kto': 'kto', }

    def __init__(self, *args, **kwargs):
        super(ZapisNaEventForm, self).__init__(*args, **kwargs)
        self.fields['kto'].required = False
        self.fields['kto'].widget = HiddenInput()

class ZapisNaEventPonownieForm(ModelForm):
    class Meta:
        model = Zapis
        fields = ['kto', 'gotowosc', 'komentarz', 'anulowany']
        labels = {'kto': 'kto', }

    def __init__(self, *args, **kwargs):
        super(ZapisNaEventPonownieForm, self).__init__(*args, **kwargs)
        self.fields['kto'].required = False
        self.fields['kto'].widget = HiddenInput()
        self.fields['anulowany'].initial = True

class ZapisNaEventUpdateForm(ModelForm):
    class Meta:
        model = Zapis
        fields = ['kto', 'gotowosc', 'komentarz', 'anulowany',]
        labels = {'kto': 'kto', 'anulowany': 'Anuluj zapis'}

    def __init__(self, *args, **kwargs):
        super(ZapisNaEventUpdateForm, self).__init__(*args, **kwargs)
        self.fields['kto'].required = False
        self.fields['kto'].widget = HiddenInput()

### wybieranie do skladu
class WyborNaEventForm(ModelForm):
    class Meta:
        model = Zapis
        fields = ['kto', 'na_co', 'wybrany']
    
    def __init__(self, *args, **kwargs):
        super(WyborNaEventForm, self).__init__(*args, **kwargs)
        self.fields['kto'].required = False
        self.fields['kto'].widget = HiddenInput()

WyborNaEventFormset = inlineformset_factory(Event, Zapis, form=WyborNaEventForm, extra=0, can_delete=False)