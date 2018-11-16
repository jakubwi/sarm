from django.forms import ModelForm, forms
from pages.models import Rekrutacja, Klasa, Killshot

class KillshotCreateForm(ModelForm):
    class Meta:
        model = Killshot
        fields = ['image', 'boss', ]
        labels = {'image': 'Dodaj screenshot (rozdzielczość 1920x1080', 'boss': 'Wpisz nazwę bossa'}

class RekrutacjaForm(ModelForm):
    class Meta:
        model = Rekrutacja
        fields = ['tank', 'heal', 'melee', 'ranged']

    def __init__(self, *args, **kwargs):
        super(RekrutacjaForm, self).__init__(*args, **kwargs)
        klasa = Klasa
        if self.instance:
            if not self.instance.klasa.tank:
                del self.fields['tank'] # removes field from form and template
            if not self.instance.klasa.heal:
                del self.fields['heal']
            if not self.instance.klasa.melee:
                del self.fields['melee']
            if not self.instance.klasa.ranged:
                del self.fields['ranged']

class TworzenieKlasyForm(ModelForm):
    class Meta:
        model = Klasa
        fields = ['name', 'icon', 'tank', 'heal', 'melee', 'ranged']
    
class RekrutacjaNowaForm(ModelForm):
    class Meta:
        model = Rekrutacja
        fields = ['klasa', 'tank', 'heal', 'melee', 'ranged']
