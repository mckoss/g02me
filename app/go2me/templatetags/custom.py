from django import template
from django.template.defaultfilters import stringfilter

from util import local

register = template.Library()

@register.filter(name='ellipsis')
@stringfilter
def ellipsis(value, arg):
    """
    Truncates a string more than arg characters and appends elipsis
    """
    try:
        length = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
    if (len(value) > length):
        return value[:length] + "..."
    else:
        return value

@register.filter(name='urlizetop')
@stringfilter
def urlizetop(value, sAttr=None):
    from django.utils.html import urlize
    "Converts URLs in plain text into clickable links - with additional attribute text inserted in <a> tags."
    value = urlize(value, nofollow=True)
    return value.replace('<a ', '<a target="_top" ')
    
# --------------------------------------------------------------------
# String utilities - format date as an "age"
# --------------------------------------------------------------------

@register.filter(name='Age')
def SAgeReq(dt):
    # Return the age (time between time of request and a date) as a string
    return SAgeDdt(local.dtNow - dt)

def SAgeDdt(ddt):
    """ Format a date as an "age" """
    if ddt.days < 0:
        return "future?"
    months = int(ddt.days*12/365)
    years = int(ddt.days/365)
    if years >= 1:
        return "%d year%s ago" % (years, SPlural(years))
    if months >= 3:
        return "%d months ago" % months 
    if ddt.days == 1:
        return "yesterday"
    if ddt.days > 1:
        return "%d days ago" % ddt.days
    hrs = int(ddt.seconds/60/60)
    if hrs >= 1:
        return "%d hour%s ago" % (hrs, SPlural(hrs))
    minutes = round(ddt.seconds/60)
    if minutes < 1:
        return "seconds ago"
    return "%d minute%s ago" % (minutes, SPlural(minutes))

def SPlural(n, sPlural="s", sSingle=''):
    return [sSingle, sPlural][n!=1]