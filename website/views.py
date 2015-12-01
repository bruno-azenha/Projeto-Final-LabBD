# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from django.db import connection

import datetime

from .forms import *
from .models import *

def executeQuery(sql_string, fetchAll):
	cursor = connection.cursor()
	cursor.execute(sql_string)
	if fetchAll:
		return (cursor.fetchall())
	else:
		return (cursor.fetchone())

def executeSQL(sql_string):
	cursor = connection.cursor()
	cursor.execute(sql_string)

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
	vendedores = executeQuery(query, True)

	vendedores_list = []
	for v in vendedores:
		v_id = v[0]
		v_nome = v[1]
		vendedores_list.append({"id": v_id, "nome": v_nome})
	
	query = "SELECT P.CODIGO, ( C.PRIMEIRONOME || ' ' || C.NOMEDOMEIO || ' ' || C.SOBRENOME ) as cliente, P.DTPEDIDO FROM PEDIDO P INNER JOIN CLIENTE C ON P.CODIGOCLIENTE = C.CODIGO WHERE P.CODIGOVENDEDOR={}".format(vendedor_id)
	pedidos = executeQuery(query, True)

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

def CreatePedido(request):

	if request.method == 'POST':
		form = PedidoForm(request.POST)
		# check whether it's valid:

		if form.is_valid():

			# Discovers the last pk
			query = "SELECT codigo FROM Pedido ORDER BY codigo DESC"
			key = int(executeQuery(query, False)[0]) + 1

			print("Last Key: {}".format(key))
			dtpedido = "to_timestamp('{:%Y-%m-%d}', 'YYYY-MM-DD')".format(datetime.datetime.now())
			dtenvio = dtpedido
			dtrecebimento = dtpedido
			codigocliente = form.cleaned_data['codigocliente']
			contacliente = form.cleaned_data['contacliente']
			numerocartaocredito = form.cleaned_data['numerocartaocredito']
			codigoconfirmacao = form.cleaned_data['codigoconfirmacao']
			codigovendedor = 287
			imposto = form.cleaned_data['imposto']
			enderecofatura = form.cleaned_data['enderecofatura']
			enderecoentrega = form.cleaned_data['enderecoentrega']
			codigotransportadora = form.cleaned_data['codigotransportadora']

			query = "INSERT INTO Pedido (codigo, dtpedido, dtenvio, dtrecebimento, codigocliente, contacliente, numerocartaocredito, codigoconfirmacao, codigovendedor, imposto, enderecofatura, enderecoentrega, codigotransportadora) values ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10} ,{11} ,{12})".format(key, dtpedido, dtenvio, dtrecebimento, codigocliente, contacliente, numerocartaocredito, codigoconfirmacao, codigovendedor, imposto, enderecofatura, enderecoentrega, codigotransportadora)
			print(query)
			print("Insert Result: {}".format(executeSQL(query)))

			return HttpResponseRedirect('/pedidos/success')

		else:
			return HttpResponseRedirect('/pedidos/fail')

	else:
		form = PedidoForm()


	return render_to_response(
		'create_pedido.html',
		{'form': form},
		context_instance=RequestContext(request)
	)

def Success(request):
	return render_to_response(
		'success.html', {},
		context_instance=RequestContext(request)
	)

def Fail(request):
	return render_to_response(
		'fail.html', {},
		context_instance=RequestContext(request)
	)