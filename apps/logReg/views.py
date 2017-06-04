# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import UserDB

def index(request):
	return render(request, 'logReg/index.html')

def process(request):
	if request.method == 'POST':
		if request.POST['logReg'] == 'register':
			response = UserDB.objects.validateReg(request.POST)
		elif request.POST['logReg'] == 'login':
			response = UserDB.objects.validateLog(request.POST)
		if not response[0]:
			for message in response[1]:
				messages.error(request, message[1])
			return redirect('logReg:index')
		else:
			request.session['user'] = {
				'id': response[1].id,
				'firstName': response[1].firstName,
				'lastName': response[1].lastName
			}
			return redirect('trips:home')
	return redirect('logReg:index')

def logout(request):
	request.session.clear()
	return redirect('logReg:index') 
		 
		