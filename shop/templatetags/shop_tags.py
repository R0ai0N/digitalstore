from django import template
from shop.models import Category, Favorite

register = template.Library()


@register.simple_tag()
def main_categories():
    return Category.objects.all()


@register.simple_tag(takes_context=True)
def query_params(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            query[key] = value
        elif key in query:
            del query[key]

        if key == 'brand' and 'model' in query:
            del query['model']

    return query.urlencode()


@register.simple_tag()
def get_favorites(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return [i.product for i in favorites]
    else:
        return []
