# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User, Travel
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def index(request):

  return render(request,'register.html')

def register(request):
    result = User.objects.validate(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/index')
    request.session['user_id'] = result.id
    return redirect('/travel')

def login(request):
    result = User.objects.login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/index')
    request.session['user_id'] = result.id
    return redirect('/travel')

def guest_login(request):
    request.session['user_id'] = 3
    request.session['username'] = "Guest"
    request.session['password'] = "123guest"
    return redirect('/travel')
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(username=username, password=password)
    # if user is not None:
    #     if user.is_active:
    #         login(request, user)
    #         return redirect('/travel')
    #     else:
    #         return redirect('/')
    # else:
    #     messages.error(request, err)
    #     return redirect('/')

def createplan(request):
    user=User.objects.get(id=request.session['user_id'])
    result = Travel.objects.validate_addtrip(user,request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    return redirect('/travel')

def addplan(request):
  if 'user_id' not in request.session:
    return redirect('/')
  current=User.objects.get(id=request.session['user_id'])
  context ={
    'user':current,
  }
  return render(request,'addplan.html',context)

def delete(request,travel_id):
    travel_plan=Travel.objects.get(id=travel_id)
    travel_plan.delete()
    return redirect('/travel')

def remove(request,travel_id):
    this_user=User.objects.get(id=request.session['user_id'])
    travel_plan=Travel.objects.get(id=travel_id)
    this_user.joiner.remove(travel_plan)
    return redirect('/travel')

def travel(request):
  if 'user_id' not in request.session:
    return redirect('/')
  current=User.objects.get(id=request.session['user_id'])
  context ={
    'user': current,
    'jointrips': current.joiner.all(),
    'travels':Travel.objects.filter(creator_id=current),
    'others': Travel.objects.all().exclude(creator_id=current)
  }
  return render(request,'travel.html',context)

def show(request,travel_id):
    current=User.objects.get(id=request.session['user_id'])
    context ={
        'travel':Travel.objects.get(id=travel_id),
        'user':current,
        'others':Travel.objects.filter(joiner=travel_id)
    }
    return render(request, 'show.html', context)
def join(request,travel_id):
    this_user=User.objects.get(id=request.session['user_id'])
    this_trip=Travel.objects.get(id=travel_id)
    this_user.joiner.add(this_trip)
    return redirect('/travel')

def logout(request):
    request.session.clear()
    return redirect('/')
