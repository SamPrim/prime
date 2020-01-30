from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Membre, discussion
from .form import NameForm
from rest_framework import viewsets 
from .serializers import *
import json
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login



# Create your views here.

class membresViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class= membreSerializer

def index(request):
    return render(request,"index.html",{})

def register(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm
    context={'form':form}
    return render(request, 'registration/register.html', context)

def home(request, id):
    listeAmis=ListeAmis()
    return render(request, 'mapage.html', {'listeAmis':listeAmis})

def ListeAmis():
    response=requests.get("http://localhost:8000/chat/api/membre/?format=json")
    liste_membre=response.json()
    return liste_membre

def room(request, id):
    return render(request, 'room.html',{})

def anime(request):
    return render(request, 'anime.html', {})
"""def index(request):
    if request.POST:
        form = NameForm(request.POST)
        if form.is_valid():
            return render(request,"listMembres.html", {})
    else:
        form = NameForm()
    return render(request,"form.html",{"form": form})"""

"""def membres(request):
    if request.POST:
        data = request.POST.copy()
        nom=data.get('name')
        name=Membre.objects.create(nom=nom)
        name.save()
    liste_membre= Membre.objects.all()

    return render(request,'listMembres.html',{'membres':liste_membre})

def home(request):
    response=requests.get("http://localhost:8000/chat/api/membre/?format=json")
    liste_membre=response.json()
    return render(request, 'index.html',{"liste":liste_membre})

def page(request, id):
    id_user= get_object_or_404(Membre, pk=id)
    return render(request, 'mapage.html', {"id":id_user})"""