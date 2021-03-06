# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.db import connection

import datetime

from .forms import *
from .models import *

def executeQuery(sql_string, fetchAll):
	cursor = connection.cursor()
	cursor.execute(sql_string)
	
	result = cursor.fetchall() if fetchAll else cursor.fetchone()
	cursor.close()
	return result

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

			attributes = '(codigo'
			values = '({}'.format(key)
			dtpedido = "to_timestamp('{:%Y-%m-%d}', 'YYYY-MM-DD')".format(datetime.datetime.now())
			dtenvio = dtpedido
			dtrecebimento = dtpedido
			attributes += ', dtpedido, dtenvio, dtrecebimento'
			values += ", {0}, {1}, {2}".format(dtpedido, dtenvio, dtrecebimento)

			codigocliente = form.cleaned_data['codigocliente']
			if codigocliente != None:
				attributes += ', codigocliente'
				values += ", {0}".format(codigocliente)

			contacliente = form.cleaned_data['contacliente']
			if contacliente != None:
				attributes += ', contacliente'
				values += ", '{0}'".format(contacliente)
			
			numerocartaocredito = form.cleaned_data['numerocartaocredito']
			if numerocartaocredito != None:
				attributes += ', numerocartaocredito'
				values += ", {0}".format(numerocartaocredito)

			codigoconfirmacao = form.cleaned_data['codigoconfirmacao']
			if codigoconfirmacao != None:
				attributes += ', codigoconfirmacao'
				values += ", '{0}'".format(codigoconfirmacao)

			codigovendedor = 287
			attributes += ', codigovendedor'
			values += ", '{0}'".format(codigovendedor)

			imposto = form.cleaned_data['imposto']
			if imposto != None:
				attributes += ', imposto'
				values += ", '{0}'".format(imposto)

			enderecofatura = form.cleaned_data['enderecofatura']
			if enderecofatura != None:
				attributes += ', enderecofatura'
				values += ", '{0}'".format(enderecofatura)

			enderecoentrega = form.cleaned_data['enderecoentrega']
			if enderecoentrega != None:
				attributes += ', enderecoentrega'
				values += ", '{0}'".format(enderecoentrega)

			codigotransportadora = form.cleaned_data['codigotransportadora']
			if codigotransportadora != None:
				attributes += ', codigotransportadora'
				values += ", '{0}'".format(codigotransportadora)

			attributes += ')'
			values += ")".format(codigotransportadora)
			query = "INSERT INTO Pedido {0} values {1}".format(attributes, values)
			print(query)
			executeSQL(query)

			return HttpResponseRedirect(reverse('success'))

		else:
			return HttpResponseRedirect(reverse('fail'))

	else:
		form = PedidoForm()


	return render_to_response(
		'create_pedido.html',
		{'form': form},
		context_instance=RequestContext(request)
	)

def ShowPedido(request):
	if request.method == 'GET':
		pedido_id = request.GET.get("pedido_id")

		query = "SELECT * FROM Pedido WHERE codigo = {}".format(pedido_id)
		pedido = executeQuery(query, True)
		print(pedido)
		data = {}
		data['pedido_id'] = pedido[0][0]
		data['dtpedido'] = pedido[0][1]
		data['dtenvio'] = pedido[0][2] 
		data['dtrecebimento'] = pedido[0][3]

		cliente = executeQuery("SELECT ( PRIMEIRONOME || ' ' || NOMEDOMEIO || ' ' || SOBRENOME ) as cliente FROM Cliente WHERE codigo = {}".format(pedido[0][4]), 0)
		data['cliente'] = cliente[0]
		data['contacliente'] = pedido[0][5] 
		data['numerocartaocredito'] = pedido[0][6] 
		data['codigoconfirmacao'] = pedido[0][7] 
		data['codigovendedor'] = pedido[0][8] 
		data['imposto'] = pedido[0][9] 
		data['enderecofatura'] = pedido[0][10]
		data['enderecoentrega'] = pedido[0][11] 
		data['codigotransportadora'] = pedido[0][12]

		self = True if data['codigovendedor'] == 287 else False

		return render_to_response(
			'show_pedido.html', {'data': data, 'self': self},
			context_instance=RequestContext(request)
	)

def UpdatePedido(request):
	if request.method == 'GET':
		pedido_id = request.GET.get("pedido_id")

		query = "SELECT * FROM Pedido WHERE codigo = {}".format(pedido_id)
		pedido = executeQuery(query, True)
		print(pedido)
		data = {}
		data['pedido_id'] = pedido[0][0]
		data['dtpedido'] = pedido[0][1]
		data['dtenvio'] = pedido[0][2] 
		data['dtrecebimento'] = pedido[0][3] 
		data['codigocliente'] = pedido[0][4] 
		data['contacliente'] = pedido[0][5] 
		data['numerocartaocredito'] = pedido[0][6] 
		data['codigoconfirmacao'] = pedido[0][7] 
		data['codigovendedor'] = pedido[0][8] 
		data['imposto'] = pedido[0][9] 
		data['enderecofatura'] = pedido[0][10]
		data['enderecoentrega'] = pedido[0][11] 
		data['codigotransportadora'] = pedido[0][12]
		form = PedidoForm(data)		

		return render_to_response(
			'update_pedido.html', {'data': data, 'form': form},
			context_instance=RequestContext(request)
		)

	else:
		form = PedidoForm(request.POST)
		# check whether it's valid:

		if form.is_valid():

			query = "UPDATE Pedido SET "
			pedido_id = request.POST.get("pedido_id")

			dtpedido = "to_timestamp('{:%Y-%m-%d}', 'YYYY-MM-DD')".format(datetime.datetime.now())
			dtenvio = dtpedido
			dtrecebimento = dtpedido
			query += "dtpedido = {0}, dtenvio = {1}, dtrecebimento = {2}".format(dtpedido, dtenvio, dtrecebimento)

			codigocliente = form.cleaned_data['codigocliente']
			query = query + ", codigocliente = {}".format(codigocliente) if codigocliente != None else query
			contacliente = form.cleaned_data['contacliente']
			query = query + ", contacliente = '{}'".format(contacliente) if contacliente != None else query
			numerocartaocredito = form.cleaned_data['numerocartaocredito']
			query = query + ", numerocartaocredito = {}".format(numerocartaocredito) if numerocartaocredito != None else query
			codigoconfirmacao = form.cleaned_data['codigoconfirmacao']
			query = query + ", codigoconfirmacao = '{}'".format(codigoconfirmacao) if codigoconfirmacao != None else query
			codigovendedor = form.cleaned_data['codigovendedor']
			query = query + ", codigovendedor = {}".format(codigovendedor) if codigovendedor != None else query
			imposto = form.cleaned_data['imposto']
			query = query + ", imposto = {}".format(imposto) if imposto != None else query
			enderecofatura = form.cleaned_data['enderecofatura']
			query = query + ", enderecofatura = {}".format(enderecofatura) if enderecofatura != None else query
			enderecoentrega = form.cleaned_data['enderecoentrega']
			query = query + ", enderecoentrega = {}".format(enderecoentrega) if enderecoentrega != None else query
			codigotransportadora = form.cleaned_data['codigotransportadora']
			query = query + ", codigotransportadora = {}".format(codigotransportadora) if codigotransportadora != None else query

			query += " WHERE codigo = {}".format(pedido_id) 
			print(query)
			executeSQL(query)

			return HttpResponseRedirect(reverse('success'))

		else:
			return HttpResponseRedirect(reverse('fail'))



def DeletePedido(request):
	pedido_id = request.GET.get("pedido_id")

	query = "DELETE FROM Pedido WHERE codigo = {}".format(pedido_id)
	pedido = executeSQL(query)

	return render_to_response(
		'success.html', {},
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

def MelhoresClientes(request):

	query = """	SELECT DISTINCT ( PRIMEIRONOME || ' ' || NOMEDOMEIO || ' ' || SOBRENOME ) as cliente, COUNT(P.codigo) "qtde"
				FROM Cliente C 
					INNER JOIN Pedido P  
					  ON C.codigo = P.codigocliente
				GROUP BY C.primeironome, C.nomedomeio, C.sobrenome 
					HAVING COUNT(P.codigo) >= 15
				ORDER BY COUNT(P.codigo) DESC"""

	clientes = executeQuery(query, True)
	melhores_clientes = []
	for c in clientes:
		c_nome = c[0]
		c_qtd = c[1]

		melhores_clientes.append({"nome": c_nome, "qtd": c_qtd})

	print(melhores_clientes)

	return render_to_response(
		'melhores-clientes.html', {'melhores_clientes': melhores_clientes},
		context_instance=RequestContext(request)
	)

def AvaliacaoVendedor(request):
	if request.method == 'GET':

		form = DataRangeForm()

		return render_to_response(
		'avaliacao-vendedor.html', {'form': form},
		context_instance=RequestContext(request))
	
	else:
		form = DataRangeForm(request.POST)

		if form.is_valid():
			dtinicio = "('{:%Y-%m-%d}', 'YYYY-MM-DD')".format(form.cleaned_data['dtinicio'])
			dtfim = "('{:%Y-%m-%d}', 'YYYY-MM-DD')".format(form.cleaned_data['dtfim'])
			print(dtinicio)

			query = """SELECT 
						SUM(D.PRECOUNITARIO*D.QUANTIDADE-D.DESCONTO) AS TOTAL,
						(V.PRIMEIRONOME || ' ' || V.NOMEDOMEIO || ' ' || V.SOBRENOME) AS NOME, V.QUOTA
						FROM DETALHESPEDIDO D
							JOIN PEDIDO P ON D.CODIGOPEDIDO = P.CODIGO 
								AND P.DTPEDIDO BETWEEN TO_DATE {0}
								AND TO_DATE {1}
							JOIN VENDEDOR V ON P.CODIGOVENDEDOR = V.CODIGO
						HAVING SUM(D.PRECOUNITARIO*D.QUANTIDADE-D.DESCONTO) >= V.QUOTA 
						GROUP BY 
							V.CODIGO, 
							(V.PRIMEIRONOME || ' ' || V.NOMEDOMEIO || ' ' || V.SOBRENOME), 
							V.QUOTA;""".format(dtinicio, dtfim)

			print(query)

			vendedores = executeQuery(query, True)
			print (vendedores)

			vendedores_list = []
			for v in vendedores:
				v_totalVendas = v[0]
				v_nome = v[1]
				v_cota = v[2]
				print (v_nome)
				vendedores_list.append({"nome": v_nome, "cota": v_cota, "total_vendas": v_totalVendas})


			return render_to_response(
				'avaliacao-vendedor.html', {'vendedores_list': vendedores_list, 'form': form},
				context_instance=RequestContext(request))
		else:
			return render_to_response(
				'fail.html', {},
				context_instance=RequestContext(request))

def CreateCliente(request):

	if request.method == 'POST':
		form = ClienteForm(request.POST)
		# check whether it's valid:

		if form.is_valid():

			# Discovers the last pk
			query = "SELECT codigo FROM Cliente ORDER BY codigo DESC"
			key = int(executeQuery(query, False)[0]) + 1

			attributes = '(codigo'
			values = '({}'.format(key)

			tratamento = form.cleaned_data['tratamento']
			if tratamento != None:
				attributes += ', tratamento'
				values += ", '{0}'".format(tratamento)
			
			primeironome = form.cleaned_data['primeironome']
			if primeironome != None:
				attributes += ', primeironome'
				values += ", '{0}'".format(primeironome)

			nomedomeio = form.cleaned_data['nomedomeio']
			if nomedomeio != None:
				attributes += ', nomedomeio'
				values += ", '{0}'".format(nomedomeio)

			sobrenome = form.cleaned_data['sobrenome']
			if sobrenome != None:
				attributes += ', sobrenome'
				values += ", '{0}'".format(sobrenome)

			sufixo = form.cleaned_data['sufixo']
			if sufixo != None:
				attributes += ', sufixo'
				values += ", '{0}'".format(sufixo)

			senha = form.cleaned_data['senha']
			if senha != None:
				attributes += ', senha'
				values += ", '{0}'".format(senha)

			attributes += ')'
			values += ')'
			query = "INSERT INTO Cliente {0} values {1}".format(attributes, values)
			print(query)
			executeSQL(query)

			return HttpResponseRedirect(reverse('success'))

		else:
			return HttpResponseRedirect(reverse('fail'))

	else:
		form = ClienteForm()

	return render_to_response(
		'create_cliente.html',
		{'form': form},
		context_instance=RequestContext(request)
	)