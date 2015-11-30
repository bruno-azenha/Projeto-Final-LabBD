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
	if request.method == 'POST':
		print("ok")
	else:
		query = "SELECT P.CODIGO, ( C.PRIMEIRONOME || ' ' || C.NOMEDOMEIO || ' ' || C.SOBRENOME ) as cliente, P.DTPEDIDO FROM PEDIDO P INNER JOIN CLIENTE C ON P.CODIGOCLIENTE = C.CODIGO WHERE P.CODIGOVENDEDOR=279"
		pedidos = executeSQL(query)
		pedidos_list = []
		for p in pedidos:
			pedido_id = p[0]
			pedido_cliente = p[1]
			pedido_data = p[2]
			print (pedido_cliente)
			pedidos_list.append({"id": pedido_id, "cliente": pedido_cliente, "data": pedido_data})

		form = PedidoForm()

	return render_to_response(
		'pedidos.html',
		{'form': form, 'pedidos_list': pedidos_list},
		context_instance=RequestContext(request)
	)




#(ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.0.171)(PORT = 1521))
