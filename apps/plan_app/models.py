# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import bcrypt
import re
from django.db import models

class UserManager(models.Manager):
    def validate(self,post_data):
        errors=[]

        if len(post_data['name'])<0:
            errors.append('please enter an valid name')
        if User.objects.filter(username=post_data['username']):
            errors.append('user name already in database')
        if len(post_data['username'])<0:
            errors.append('please enter a username')
        if len(post_data['password'])<8:
            errors.append('password needs to be more than 8 characters')
        if post_data['password']!=post_data['cpassword']:
            errors.append('passwords do not match')

        if not errors:
            hashed_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(
                name=post_data['name'],
                username=post_data['username'],
                password = hashed_pw
            )
            return new_user
        return errors

    def login(self,post_data):
        errors = []
        if len(self.filter(username=post_data['username'])) > 0:
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('username/password incorrect')
        else:
            errors.append('username/password incorrect')
        if errors:
            return errors
        return user

class User(models.Model):
    name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()


class TravelManager(models.Manager):
    def validate_addtrip(self,user, post_data):
        errors=[]
        if len(post_data['destination'])<0:
            errors.append('please enter a destination')
        if len(post_data['plan'])<0:
            errors.append('please enter a description')
        if not errors:
            new_trip = Travel.objects.create(
                destination=post_data['destination'],
                description=post_data['plan'],
                travelstart=post_data['travelstart'],
                travelend=post_data['travelend'],
                creator= user
            )
            return new_trip
        return errors

class Travel(models.Model):
    destination= models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    travelstart = models.DateField(default="")
    travelend = models.DateField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="planner",)
    joiner = models.ManyToManyField(User, related_name="joiner")
    objects=TravelManager()
