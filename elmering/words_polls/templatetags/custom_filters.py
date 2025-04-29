from django import template


register = template.Library()


@register.filter
def format_translation(translations):
    if not translations.exists():
        return ''
    words: list = [t.word for t in translations]
    return ", ".join(words) + "."
