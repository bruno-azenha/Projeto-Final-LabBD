# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.db import connection

from .forms import *
from .models import *

def executeSQL(sql_string):
	cursor = connection.cursor()
	cursor.execute(sql_string)
	return (cursor.fetchall())

# Create your views here.
def LandingPage(request):

	return render_to_response(
		'index.html',
		{},
		context_instance=RequestContext(request)
	)

def Pedidos(request):
	self = False
	if request.method == 'POST':
		vendedor_id = request.POST.get("vendedor_id")
		if vendedor_id == None: 
			self = True
			vendedor_id = 287
		if int(vendedor_id) == 287:
			self = True

	else:
		vendedor_id = 287
		self = True

	print(vendedor_id)

	query = "SELECT CODIGO, ( PRIMEIRONOME || ' ' || NOMEDOMEIO || ' ' || SOBRENOME ) as vendedor FROM VENDEDOR;"
	vendedores = executeSQL(query)

	vendedores_list = []
	for v in vendedores:
		v_id = v[0]
		v_nome = v[1]
		vendedores_list.append({"id": v_id, "nome": v_nome})
	
	query = "SELECT P.CODIGO, ( C.PRIMEIRONOME || ' ' || C.NOMEDOMEIO || ' ' || C.SOBRENOME ) as cliente, P.DTPEDIDO FROM PEDIDO P INNER JOIN CLIENTE C ON P.CODIGOCLIENTE = C.CODIGO WHERE P.CODIGOVENDEDOR={}".format(vendedor_id)
	pedidos = executeSQL(query)

	pedidos_list = []
	for p in pedidos:
		p_id = p[0]
		p_cliente = p[1]
		p_data = p[2]
		pedidos_list.append({"id": p_id, "cliente": p_cliente, "data": p_data})

	return render_to_response(
		'pedidos.html',
		{'vendedores_list': vendedores_list, 'pedidos_list': pedidos_list, 'self': self},
		context_instance=RequestContext(request)
	)




#(ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.0.171)(PORT = 1521))
