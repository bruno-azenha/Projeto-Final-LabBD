from django.http import HttpResponse
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
	html = "<html><body>{}</body></html>".format(result)
	return HttpResponse(html)




#(ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.0.171)(PORT = 1521))
