from django import template
from website.models import Category, God, Month, Quarter, Polugodie

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all().order_by('pk')


@register.simple_tag()
def get_years():
    return God.objects.all()


@register.simple_tag()
def get_months():
    return Month.objects.all()


@register.simple_tag()
def get_quarters():
    return Quarter.objects.all()


@register.simple_tag()
def get_polugodie():
    return Polugodie.objects.all()
