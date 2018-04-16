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
