# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.db import connection

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
	return render_to_response(
		'pedidos.html',
		{},
		context_instance=RequestContext(request)
	)




#(ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.0.171)(PORT = 1521))
