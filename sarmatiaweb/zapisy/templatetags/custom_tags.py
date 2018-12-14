from django import template
register = template.Library()

from zapisy.models import Event, Zapis

@register.simple_tag
def check_zapis(event, user):
    event = event
    user = user
    zapis_usera = Zapis.objects.filter(kto=user, na_co=event)
    if zapis_usera:
        return True
    else:
        return False