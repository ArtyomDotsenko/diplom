from django import template
from website.models import Category, God, Month

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_years():
    return God.objects.all()


@register.simple_tag()
def get_months():
    return Month.objects.all()
