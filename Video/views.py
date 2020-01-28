from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Membre, discussion
from .form import NameForm
from rest_framework import viewsets 
from .serializers import *
import json
import requests


# Create your views here.

class membresViewSet(viewsets.ModelViewSet):
    queryset = Membre.objects.all()
    serializer_class= membreSerializer

def index(request):
    if request.POST:
        form = NameForm(request.POST)
        if form.is_valid():
            return render(request,"listMembres.html", {})
    else:
        form = NameForm()
    return render(request,"form.html",{"form": form})

def membres(request):
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
    return render(request, 'mapage.html', {"id":id_user})