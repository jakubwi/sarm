from django.forms import ModelForm, forms, modelformset_factory, HiddenInput, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from .models import Wymagania, Event, Zapis
from users.models import CustomUser
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

### create forms
class EventCreateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['nazwa', 'kiedy_dzien', 'kiedy_godzina', 'opis', 'miejsca', 'alty']
        widgets = {'kiedy_dzien': DatePickerInput(format='%Y-%m-%d'),
                    'kiedy_godzina': TimePickerInput(format='%H:%M:%S'),}

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