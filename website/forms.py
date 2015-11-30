# -*- coding: utf-8 -*-
from django import forms

class PedidoForm(forms.Form):
	dtpedido = forms.DateField(label='Data do Pedido', required=True)
	dtenvio = forms.DateField(label='Data de Envio')
	dtrecebimento = forms.DateField(label='Data de Recebimento')
	codigocliente = forms.IntegerField(label='Código Cliente', required=True)
	contacliente = forms.CharField(label='Conta Cliente', max_length=15)
	numerocartaocredito = forms.IntegerField(label='Cartão')
	codigoconfirmacao = forms.CharField(label='Código de Confirmação', max_length=15)
	codigovendedor = forms.IntegerField(label='Código Vendedor')
	imposto = forms.IntegerField(label='Imposto')
	enderecofatura = forms.IntegerField(label='Endereço de Fatura')
	enderecoentrega = forms.IntegerField(label='Endereço de Entrega')
	codigotransportadora = forms.IntegerField(label='Código da Transportadora')

