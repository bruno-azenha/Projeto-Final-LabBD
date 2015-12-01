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
    url(r'^pedidos/create', CreatePedido, name="create_pedido"),
    url(r'^pedidos/show', ShowPedido, name="show_pedido"),
    url(r'^pedidos/update', UpdatePedido, name="update_pedido"),
    url(r'^pedidos/delete', DeletePedido, name="delete_pedido"),
    url(r'^pedidos/success', Success, name="success"),
    url(r'^pedidos/fail', Fail, name="fail"),
    url(r'^clientes/create', CreateCliente, name="create_cliente"),
    url(r'^melhores-clientes/', MelhoresClientes, name="melhores-clientes"),
    url(r'^avaliacao-vendedor/', AvaliacaoVendedor, name="avaliacao-vendedor"),

)
