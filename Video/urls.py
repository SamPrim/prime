from django.urls import path, include
from . import views

app_name="chat"

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'membre', views.membresViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('list', views.membres, name='listes'),
    path('<int:id>/home', views.page, name='page'),
    path('api/', include(router.urls)),
]