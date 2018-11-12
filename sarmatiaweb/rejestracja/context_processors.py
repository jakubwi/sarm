from rejestracja.models import Podanie

def ilosc_podan(request):
    lista_podan = Podanie.objects.order_by('-date')
    list_podan_bez_decyzji = []
    for i in lista_podan:
        if not i.accepted and not i.rejected:
            list_podan_bez_decyzji.append(i)
    ilosc_podan = len(list_podan_bez_decyzji)
    return {'ilosc_podan': ilosc_podan}