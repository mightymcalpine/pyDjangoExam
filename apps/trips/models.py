# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..logReg.models import UserDB
import datetime
 
class TripsDBManager(models.Manager):
	def createTrip(self, postData, id):
		errors = []
		if len(postData['destination']) < 3:
			errors.append(['destination', 'Trip destination must be at least 3 characters'])
		if len(postData['description']) < 1:
			errors.append(['description', 'Please enter a description of your trip'])
		# could refactor these two into on statement
		if len(postData['startDate']) < 10:
			errors.append(['startDate', 'Please enter a valid date'])
		if len(postData['endDate']) < 10:
			errors.append(['endDate', 'Please enter a valid date'])
		if errors:
			return [False, errors]
		elif datetime.datetime.now() > datetime.datetime.strptime(postData['startDate'].encode(), '%Y-%m-%d'):
			errors.append(['startDate', 'Trip start date must be after today.'])
			return [False, errors]
		elif postData['endDate'] < postData['startDate']:
			errors.append(['endDate', 'Trip end date must be after the trip start date.'])
			return [False, errors]
		else:
			newTrip = TripsDB.objects.create(destination = postData['destination'], plan = postData['description'], startDate = postData['startDate'], endDate = postData['endDate'], plannedBy = UserDB.objects.get(id=id))
			return [True, newTrip]
	
	def joinTrips(self, id, userID):
		userID = UserDB.objects.get(id=userID)
		tripID = TripsDB.objects.get(id=id)
		tripID.usersJoined.add(userID)

# Create your models here.
class TripsDB(models.Model):
	destination = models.CharField(max_length = 128)
	plan = models.TextField()
	plannedBy = models.ForeignKey(UserDB, related_name="tripsPlanned")
	usersJoined = models.ManyToManyField(UserDB, related_name="tripsJoined")
	startDate = models.DateField()
	endDate = models.DateField()
	createdAt = models.DateTimeField(auto_now_add=True)
	updateAt = models.DateTimeField(auto_now=True)
	objects = TripsDBManager()
	