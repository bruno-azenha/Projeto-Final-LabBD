# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from django.db import connection



class PedidoForm(forms.Form):
	
	cursor = connection.cursor()
	query = "SELECT codigo, ( PRIMEIRONOME || ' ' || NOMEDOMEIO || ' ' || SOBRENOME ) as nome FROM Cliente"
	cursor.execute(query)
	clientes = cursor.fetchall()
	choices = []
	for c in clientes:
		choices.insert(0, c)

	dtenvio = forms.DateTimeField(label='Data de Envio', required=False, widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": True}))
	dtrecebimento = forms.DateTimeField(label='Data de Recebimento', required=False, widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": True}))
	codigocliente = forms.ChoiceField(label='Cliente', required=True, choices=choices)
	contacliente = forms.CharField(label='Conta Cliente', required=False, max_length=15)
	numerocartaocredito = forms.IntegerField(label='Cartão', required=False)
	codigoconfirmacao = forms.CharField(label='Código de Confirmação', required=False, max_length=15)
	codigovendedor = forms.IntegerField(label='Código Vendedor', required=False)
	imposto = forms.FloatField(label='Imposto', required=False)
	enderecofatura = forms.IntegerField(label='Endereço de Fatura', required=False)
	enderecoentrega = forms.IntegerField(label='Endereço de Entrega', required=False)
	codigotransportadora = forms.IntegerField(label='Código da Transportadora', required=False)

class DataRangeForm(forms.Form):
	dtinicio = forms.DateTimeField(label='Data Inicial', required=False, widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": True}))
	dtfim = forms.DateTimeField(label='Data Final', required=False, widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": True}))

class ClienteForm(forms.Form):
	tratamento = forms.CharField(label='Tratamento', required=False, max_length=8)
	primeironome = forms.CharField(label='Primeiro Nome', required=True, max_length=50)
	nomedomeio = forms.CharField(label='Nome do Meio', required=False, max_length=50)
	sobrenome = forms.CharField(label='Sobrenome', required=True, max_length=50)
	sufixo = forms.CharField(label='Sufixo', required=False, max_length=10)
	senha = forms.CharField(label='Senha', required=True, max_length=128)
