# coding: utf-8
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

def active_page(request, view_name):
    from django.core.urlresolvers import resolve, Resolver404
    if not request:
        return ""
    try:
        return "active" if resolve(request.path_info).url_name in view_name else ""
    except Resolver404:
        return ""

@register.filter(name='vote_style')
@stringfilter
def vote_style(value):
    vote = value.encode('utf-8')
    if vote == 'בעד':
        return "yay"
    elif vote == 'נגד':
        return "nay"
    else:
        return "abstain"


register.simple_tag(active_page)
#register.filter('vote_style', vote_style)

