from django.test import TestCase

from Video.models import Membre

# Create your tests here.

class MembreExist(TestCase):
    
    def membre_exist(self):
        m=Membre()
        self.assertIs(m, False)
