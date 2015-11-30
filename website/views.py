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
def Test(request):
	sql_string = request.GET.get('query')
	print(sql_string)
	result = executeSQL(sql_string)
	print(result)

	return render_to_response(
		'index.html',
		{'query_result': result},
		context_instance=RequestContext(request)
	)




#(ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.0.171)(PORT = 1521))
