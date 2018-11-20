from django.forms import ModelForm, forms
from django import forms
from django.contrib.auth.models import User
from rejestracja.models import Podanie, PodanieKomentarze, Serwer, Rasa, Rola
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

class SerwerForm(ModelForm):
        class Meta:
                model = Serwer
                fields = ['name',]
                labels = {'name': 'Nazwa nowego serwera'}

class RasaForm(ModelForm):
        class Meta:
                model = Rasa
                fields = ['name',]
                labels = {'name': 'Nazwa nowej rasy'}

class RolaForm(ModelForm):
        class Meta:
                model = Rola
                fields = ['name',]
                labels = {'name': 'Nazwa nowej roli'}

class PodanieSocialForm(ModelForm):
        def clean(self):
                cleaned_data = self.cleaned_data # individual field's clean methods have already been called
                email = cleaned_data.get("email")
                emailConfirm = cleaned_data.get("emailConfirm")
                if email != emailConfirm:
                        raise forms.ValidationError("Wprowadź dwukrotnie poprawny adres e-mail")

                return cleaned_data

        class Meta:
                model = Podanie
                fields = ['name','serwer','rasa', 'klasa','mainspec','offspec','infoGildie','infoOgolne','plec','battleTag','email','emailConfirm',]
                labels = {'name': 'Nazwa postaci Main',
                        'serwer': 'Wybierz serwer',
                        'rasa': 'Wybierz rasę', 
                        'klasa': 'Wybierz klasę',
                        'mainspec': 'Wybierz Main Spec',
                        'offspec': 'Wybierz Off Spec',
                        'infoGildie': 'Gildie',
                        'infoOgolne': 'O sobie',
                        'plec': 'Wybierz płeć',
                        'battleTag': 'BattleTag [format: name#1234]',
                        'email': 'Podaj adres e-mail',
                        'emailConfirm': 'Podaj adres ponownie w celu werfikacji',
                }
                help_texts = {'mainspec': 'W naszej gildii każda postać musi mieć przydzieloną specjalizację Main i Off. Decyduje to o priorytecie lootu na raidach',
                        'infoGildie': 'Czy byłeś już w jakis innych gildiach? Jeśli tak to dlaczego je opuściłeś?',
                        'infoOgolne': 'Napisz coś o sobie! (np wiek, czym się zajmujesz, etc)',
                        'plec': 'Twoją, nie postaci',
                        'battleTag': 'BattleTag MUSI być poprawny. Jeśli będziemy chcieli się z tobą skontaktować zrobimy to za pomocą BattleTaga',
                        'email': 'Adres email MUSI być poprawny. Na podanego maila otrzymasz wynik postępowania rekrutacyjnego, a w przypadku przyjęcia - hasło do twojego konta na naszej stronie',
                        }



class PodanieRaidForm(ModelForm):
        def clean(self):
                cleaned_data = self.cleaned_data # individual field's clean methods have already been called
                email = cleaned_data.get("email")
                emailConfirm = cleaned_data.get("emailConfirm")
                if email != emailConfirm:
                        raise forms.ValidationError("Wprowadź dwukrotnie poprawny adres e-mail")

                return cleaned_data

        class Meta:
                model = Podanie
                fields = ['name','serwer','rasa', 'klasa','mainspec','offspec','infoRaidDoswiadczenie','infoRaidWiedza','infoRaidDni','infoGildie','infoOgolne','plec','battleTag','email','emailConfirm',]
                labels = {'name': 'Nazwa postaci Main',
                        'serwer': 'Wybierz serwer',
                        'rasa': 'Wybierz rasę', 
                        'klasa': 'Wybierz klasę',
                        'mainspec': 'Wybierz Main Spec',
                        'offspec': 'Wybierz Off Spec',
                        'infoRaidDoswiadczenie': 'Doświadczenie',
                        'infoRaidWiedza': 'Wiedza',
                        'infoRaidDni': 'Dni raidowe',
                        'infoGildie': 'Gildie',
                        'infoOgolne': 'O sobie',
                        'plec': 'Wybierz płeć',
                        'battleTag': 'BattleTag [format: name#1234]',
                        'email': 'Podaj adres e-mail',
                        'emailConfirm': 'Podaj adres ponownie w celu werfikacji',
                }
                help_texts = {'mainspec': 'W naszej gildii każda postać musi mieć przydzieloną specjalizację Main i Off. Decyduje to o priorytecie lootu na raidach',
                        'infoRaidDoswiadczenie': 'Opisz swoje doświadczenie raidowe. Proszę nie podawać tu doświadczenia z pirackich serwerów',
                        'infoRaidWiedza': 'Skąd czerpiesz wiedzę na temat swojej klasy/speca? Czy uważasz, że twoja postać jest gotowa do raidowania?',
                        'infoRaidDni': 'W jakie dni tygodnia jesteś w stanie rajdować? Pamiętaj nasze rajdy zazwyczaj trwają od godziny 20:00 do 23 lub 24 czasu polskiego (serwera)',
                        'infoGildie': 'Czy byłeś już w jakis innych gildiach? Jeśli tak to dlaczego je opuściłeś?',
                        'infoOgolne': 'Napisz coś o sobie! (np wiek, czym się zajmujesz, etc)',
                        'plec': 'Twoją, nie postaci',
                        'battleTag': 'BattleTag MUSI być poprawny. Jeśli będziemy chcieli się z tobą skontaktować zrobimy to za pomocą BattleTaga',
                        'email': 'Adres email MUSI być poprawny. Na podanego maila otrzymasz wynik postępowania rekrutacyjnego, a w przypadku przyjęcia - hasło do twojego konta na naszej stronie',
                        }


class PodanieKomentarzeForm(ModelForm):
        class Meta:
                model = PodanieKomentarze
                fields = ['comment',]
                labels = {'comment': 'Dodaj komentarz'}
                widgets = {'comment': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }