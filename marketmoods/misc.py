import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

import csv,ystockquote
from valence.models import Company, Article

companies_with_articles = []
companies_to_delete = []

for art in Article.objects.all():
    if art.company not in companies_with_articles:
        companies_with_articles.append(art.company)

for co in Company.objects.all():
    if co not in companies_with_articles:
        companies_to_delete.append(co)

for co in companies_to_delete:
    co.delete()