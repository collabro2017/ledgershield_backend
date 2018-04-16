from django.conf.urls import url
from .views import pages, exchange, transaction

urlpatterns = [
    url(r'exchange/(?P<deposit>[^\/]+)$', exchange.index, name='exchange' ),
    url(r'tx/status/(?P<order_id>[^\/]+)$', transaction.index, name='txstatus'),
    url(r'about/', pages.about, name='about'),
    url(r'faq/', pages.faq, name='faq'),
    url(r'service-fee/', pages.serice_fee, name='service-fee'),
    url(r'contact-us/', pages.contact_us, name='contact-us'),
    url(r'^$', pages.index, name='home')

]