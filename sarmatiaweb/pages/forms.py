from django.forms import ModelForm, forms, modelformset_factory, HiddenInput
from pages.models import Rekrutacja, Klasa, Killshot, Onas

class OnasUpdateForm(ModelForm):
    class Meta:
        model = Onas
        fields = ['text',]
        labels = {'text': '',}

class KillshotCreateForm(ModelForm):
    class Meta:
        model = Killshot
        fields = ['image', 'boss', ]
        labels = {'image': 'Dodaj screenshot (rozdzielczość 1920x1080)', 'boss': 'Wpisz nazwę bossa'}

class RekrutacjaForm(ModelForm):
    class Meta:
        model = Rekrutacja
        fields = ['klasa', 'tank', 'heal', 'melee', 'ranged']
        labels = {'klasa': '', 'tank': 'Tank', 'heal': 'Heal', 'melee': 'Melee', 'ranged': 'Ranged',}

    def __init__(self, instance, *args, **kwargs):
        super(RekrutacjaForm, self).__init__(instance=instance, *args, **kwargs)
        self.fields['klasa'].required = False
        self.fields['klasa'].widget = HiddenInput()
        if not instance.klasa.tank:
            del self.fields['tank']
        if not instance.klasa.heal:
            del self.fields['heal']
        if not instance.klasa.melee:
            del self.fields['melee']
        if not instance.klasa.ranged:
            del self.fields['ranged']

RekrutacjaFormSet = modelformset_factory(Rekrutacja, form=RekrutacjaForm, extra=0)

class TworzenieKlasyForm(ModelForm):
    class Meta:
        model = Klasa
        fields = ['name', 'icon', 'tank', 'heal', 'melee', 'ranged']
    
class RekrutacjaNowaForm(ModelForm):
    class Meta:
        model = Rekrutacja
        fields = ['klasa', 'tank', 'heal', 'melee', 'ranged']
