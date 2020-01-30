from django.urls import path, include
from . import views

app_name="chat"

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'membre', views.membresViewSet)

urlpatterns = [
    #path('', views.home, name='home'),
    path('<int:id>/home', views.home, name='mapage'),
    path('api/', include(router.urls)),
    path('<int:id>', views.room, name='room')
]
"""path('list', views.membres, name='listes'),

,"""