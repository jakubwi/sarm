from django.forms import ModelForm, forms, modelformset_factory, HiddenInput, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from .models import Expansion, Raid, Boss

### create forms
class ExpansionCreateForm(ModelForm):
    class Meta:
        model = Expansion
        fields = ['name', 'position', 'aktualny']
        labels = {'name': 'Nazwa', 'position': 'Numer dodatku',}
        help_texts = {'position': '0-Vanilla, 1-TBC, 2-WotLK, 3-Cata, 4-MoP, 5-WoD, 6-Legion, 7-BfA, itd.',
                        'aktualny': 'Zaznacz, jeśli jest to aktualny dodatek'}

class RaidCreateForm(ModelForm):
    class Meta:
        model = Raid
        fields = ['name', 'expansion', 'position', 'aktualny']
        labels = {'name': 'Nazwa', 'expansion': 'Dodatek', 'position': 'Pozycja na liście',}



### update forms
class ExpansionUpdateForm(ModelForm):
    class Meta:
        model = Raid
        fields = ['name', 'position', 'aktualny']
        labels = {'name': 'Nazwa', 'position': 'Numer dodatku',}
        help_texts = {'position': '0-Vanilla, 1-TBC, 2-WotLK, 3-Cata, 4-MoP, 5-WoD, 6-Legion, 7-BfA, itd.',
                        'aktualny': 'Zaznacz, jeśli jest to aktualny dodatek'}

class RaidUpdateForm(ModelForm):
    class Meta:
        model = Raid
        fields = ['name', 'expansion', 'position', 'aktualny']
        labels = {'name': 'Nazwa', 'expansion': 'Dodatek', 'position': 'Pozycja na liście',}


class BossUpdateForm(ModelForm):
    class Meta:
        model = Boss
        fields = ['name', 'raid', 'position', 'normal', 'heroic', 'mythic']
        labels = {'name': 'Nazwa', 'raid': 'Raid', 'position': 'Pozycja na liście',}

    def __init__(self, *args, **kwargs):
        super(BossUpdateForm, self).__init__(*args, **kwargs)
        self.fields['raid'].required = False
        self.fields['raid'].widget = HiddenInput()

### RAID UPDATE FORMSET (INLINE WITH BOSS UPDATE)
RaidUpdateFormset = inlineformset_factory(Raid, Boss, form=BossUpdateForm, extra=0)
