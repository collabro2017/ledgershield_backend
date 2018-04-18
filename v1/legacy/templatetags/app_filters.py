from django import template
register = template.Library()


@register.filter('faddress')
def filter_address(obj, arg):
    key = 'dest_addr_{}'.format(arg)
    if key in obj:
        return obj[key]
    return ''


@register.filter('fshare')
def filter_share(obj, arg):
    key = 'dest_amount_{}'.format(arg)
    if key in obj:
        return obj[key]
    return ''


@register.filter('error')
def filter_error(obj, key):
    try:
        return obj[key]
    except IndexError:
        return ''


@register.simple_tag(name='index_exists')
def index_exists(obj, k):
    try:
        return obj[k]
    except IndexError:
        return False