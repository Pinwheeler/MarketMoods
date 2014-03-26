import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

from valence.models import Valence

valences = Valence.objects.filter(valence=0)
for val in valences:
	val.delete()