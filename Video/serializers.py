from rest_framework import serializers
from .models import *

class membreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Membre
        fields = ('id','nom')
