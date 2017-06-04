# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt

nameREG = re.compile(r'^[a-zA-Z-]\S{2,64}$')
emailREG = re.compile(r'^[a-zA-Z0-9.+-_]+@[a-zA-Z0-9._-]+\.[a-zA-Z]*$')
pwREG = re.compile(r'^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{7,})\S$')


class UserDBChief(models.Manager):
	def encrpytPW(self, password):
		return bcrypt.hashpw(password, bcrypt.gensalt())
	
	def validateReg(self, postData):
		errors = []
		if not re.match(nameREG, postData['firstName']):
			errors.append(['firstName', 'oops first name must be at least 2 characters, letters only.'])
		if not re.match(nameREG, postData['lastName']):
			errors.append(['lastName', 'oops last name must be at least 2 characters, letters only.'])
		if not re.match(emailREG, postData['email']):
			errors.append(['email', 'oops please enter a valid email address'])
		if not re.match(pwREG, postData['pwHash']):
			errors.append(['pwHash', 'oops password must have at least 8 characters, 1 lowercase letter, 1 uppercase letter, and a number'])
		if not postData['pwConfirm'] == postData['pwHash']:
			errors.append(['pwConfirm', "oops your passwords don't match"])
		if errors:
			return [False, errors]
		else:
			existingUser = UserDB.objects.filter(email=postData['email'])
			if existingUser:
				errors.append(['existingUser', 'oops the email you entered is already registered. Please try a different email'])
				return [False, errors]
			newUser = UserDB(firstName = postData['firstName'], lastName = postData['lastName'], email = postData['email'])
			newUser.pwHash = self.encrpytPW(postData['pwHash'].encode())
			newUser.save()
			# ****** CHECK DATA SECTION *******
			print '*'*50
			print newUser
			print 'pwHash:', newUser.pwHash
			print '*'*50
			# ****** END CHECK *******
			return [True, newUser]
	
	def validateLog(self, postData):
		errors = []
		if not re.match(emailREG, postData['email']) or len(postData['pwHash']) < 8:
			errors.append(['email', 'the email or password you entered is incorrect'])
			return [False, errors]
		try:
			existingUser = UserDB.objects.get(email=postData['email'])
		except:
			errors.append(['email', 'the email or password you entered is incorrect'])
			return [False, errors]
			
		if not existingUser:
			errors.append(['existingUser', 'the email or password you entered is incorrect'])
		# elif not bcrypt.checkpw(postData['pwHash'].encode(), existingUser.pwHash.encode()):
		if bcrypt.hashpw(postData['pwHash'].encode(), existingUser.pwHash.encode()) != existingUser.pwHash:
			errors.append(['existingUser', 'the email or password you entered is incorrect'])
		if errors:
			return [False, errors]
		else:			
			# ****** CHECK DATA SECTION *******
			print '*'*50
			print existingUser
			print '*'*50
			# ****** END CHECK *******
			return [True, existingUser]
			
class UserDB(models.Model):
	firstName = models.CharField(max_length = 64)
	lastName = models.CharField(max_length = 64)
	email = models.CharField(max_length = 128)
	pwHash = models.CharField(max_length = 255)
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)
	
	objects = UserDBChief()
	
	def __str__(self):
		return 'ID: %s | FirstName: %s | LastName: %s | Email: %s' % (self.id, self.firstName, self.lastName, self.email)
	