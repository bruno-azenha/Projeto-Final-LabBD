from django.conf.urls import patterns, include, url
from django.contrib import admin
from website.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Proj_LabDB.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', LandingPage, name="landing_page"),
    url(r'^pedidos/$', Pedidos, name="pedidos"),
    url(r'^pedidos/new', CreatePedido, name="create_pedido"),
    url(r'^pedidos/success', Success, name="success"),
    url(r'^pedidos/fail', Fail, name="fail"),
)
