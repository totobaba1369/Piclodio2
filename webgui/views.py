#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from webgui.models import Rpinfo, Webradio, Player, Alarmclock
from webgui.forms import WebradioForm
import time

#---------------------------------
#   Show the homepage
#---------------------------------
def homepage(request):
    rpiInfo = Rpinfo()
    radio = Webradio.objects.get(selected=1)
    player = Player()
    return render(request,'homepage.html',{ 'rpinfo': rpiInfo,
                                            'radio': radio,
                                            'player': player})

#---------------------------------
#   Show list of web radio in db
#---------------------------------
def webradio(request):
    listRadio = Webradio.objects.all()
    return render(request,'webradio.html', {'listradio':listRadio})

#---------------------------------
#   Form to add new web radio
#---------------------------------
def addwebradio(request):
    if request.method == 'POST': # If the form has been submitted...
        form = WebradioForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # save web radio
            form.instance.selected=False;
            form.save()
            return redirect('/webradio/')
    else:
        form = WebradioForm() # An unbound form

    return render(request, 'addwebradio.html', { 'form': form,})

def deleteWebRadio(request,id):
    radio = Webradio.objects.get(id=id)
    radio.delete()
    return redirect('/webradio/')

        
def play(request,id):
    # get actual selected radio
    selectedradio = Webradio.objects.get(selected=1)
    # unselect it
    selectedradio.selected=False
    selectedradio.save()
    # set the new selected radio
    radio = Webradio.objects.get(id=id)
    radio.selected=True
    radio.save()
    player = Player()
    player.play(radio)
    return redirect('/')

def stop(request):
    player = Player()
    player.stop()
    # sleep to be sure the process have been killed
    time.sleep(1)
    return redirect('/')

def alarmclock(request):
    listAlarm = Alarmclock.objects.all()
    return render(request, 'alarmclock.html',{'listAlarm': listAlarm,})