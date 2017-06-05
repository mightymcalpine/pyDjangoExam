# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt

nameREG = re.compile(r'^[a-zA-Z ]+$')
emailREG = re.compile(r'^[a-zA-Z0-9.+-_]+@[a-zA-Z0-9._-]+\.[a-zA-Z]*$')
pwREG = re.compile(r'^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{7,})\S$')


class UserDBManager(models.Manager):
	def encrpytPW(self, password):
		return bcrypt.hashpw(password, bcrypt.gensalt())
	
	def validateReg(self, postData):
		errors = []
		if not re.match(nameREG, postData['name']):
			errors.append(['name', 'oops name must be at least 2 characters, letters only.'])
		if not re.match(nameREG, postData['username']):
			errors.append(['username', 'oops username must be at least 2 characters, letters only.'])
		if not re.match(emailREG, postData['email']):
			errors.append(['email', 'oops please enter a valid email address'])
		if not re.match(pwREG, postData['pwHash']):
			errors.append(['pwHash', 'oops password must have at least 8 characters, 1 lowercase letter, 1 uppercase letter, and a number'])
		if not postData['pwConfirm'] == postData['pwHash']:
			errors.append(['pwConfirm', "oops your passwords don't match"])
		if errors:
			return [False, errors]
		else:
			existingUser = UserDB.objects.filter(username=postData['username'])
			if existingUser:
				errors.append(['existingUser', 'oops the username you entered is already registered. Please try a different username'])
				return [False, errors]
			newUser = UserDB(name = postData['name'], username = postData['username'], email = postData['email'])
			newUser.pwHash = self.encrpytPW(postData['pwHash'].encode())
			newUser.save()
			return [True, newUser]
	
	def validateLog(self, postData):
		errors = []
		if not re.match(nameREG, postData['username']) or len(postData['pwHash']) < 8:
			errors.append(['username', 'the username or password you entered is incorrect'])
			return [False, errors]
		try:
			existingUser = UserDB.objects.get(username=postData['username'])
		except:
			errors.append(['username', 'the username or password you entered is incorrect'])
			return [False, errors]
			
		if not existingUser:
			errors.append(['existingUser', 'the username or password you entered is incorrect'])
		if bcrypt.hashpw(postData['pwHash'].encode(), existingUser.pwHash.encode()) != existingUser.pwHash:
			errors.append(['existingUser', 'the username or password you entered is incorrect'])
		if errors:
			return [False, errors]
		else:			
			return [True, existingUser]
			
class UserDB(models.Model):
	name = models.CharField(max_length = 128)
	username = models.CharField(max_length = 128)
	email = models.CharField(max_length = 128)
	pwHash = models.CharField(max_length = 255)
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)
	
	objects = UserDBManager()
	
	def __str__(self):
		return 'ID: %s | name: %s | username: %s | Email: %s' % (self.id, self.name, self.username, self.email)
	