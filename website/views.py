from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

import cx_Oracle

from .models import *

# Create your views here.
def Test(request):
	ip = 'grad.icmc.usp.br'
	port = 15214
	SID = 'orcl14'
	dsn_tns = cx_Oracle.makedsn(ip, port, SID)

	con = cx_Oracle.connect('gt2', 'gt2', dsn_tns)


	html = "<html><body>It is now {}.</body></html>".format(con.version)
	return HttpResponse(html)


#(ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.0.171)(PORT = 1521))
