# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import TripsDB, UserDB

# *** PAGE RENDERS ***
def home(request):
	if 'user' in request.session:
		currentUser = request.session['user']['id']
		context = {
			'yourTrips': TripsDB.objects.filter(plannedBy=currentUser).order_by('startDate'),
			'allTrips': TripsDB.objects.exclude(plannedBy=currentUser).exclude(usersJoined=currentUser).order_by('startDate'),
			'joinedTrips': UserDB.objects.get(id=currentUser).tripsJoined.all()
		}
		return render(request, 'trips/home.html', context)
	return redirect('logReg:index')

def newTrip(request):
	return render(request, 'trips/newtrip.html')

def tripProfile(request, id):
	if 'user' in request.session:
		context = {
			'thisTrip': TripsDB.objects.filter(id=id),
			'joined': TripsDB.objects.get(id=id).usersJoined.all()
		}
		return render(request, 'trips/tripprofile.html', context)
	return redirect('logReg:index')

#  *** REDIRECTS ***
def addTrip(request):
	if 'user' in request.session:
		if request.method == 'POST':		
			response = TripsDB.objects.createTrip(request.POST, request.session['user']['id'])
			if not response[0]:
				for message in response[1]:				
					messages.error(request, message[1])
				return redirect('trips:newTrip')
			else:
				# if response[0]:
				return redirect('trips:home')
		return redirect('trips:home')
	return redirect('logReg:index')

def join(request, id):
	if 'user' in request.session:
		TripsDB.objects.joinTrips(id, request.session['user']['id'])
		return redirect('trips:home')
	return redirect('logReg:index')