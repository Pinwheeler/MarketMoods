from django.contrib import admin

# Register your models here.
from valence.models import Company, Article, Price, Valence

class CompanyAdmin(admin.ModelAdmin):
	list_display = ('ticker','name','industry','super_sector','sub_sector')
	list_filter = ('industry','super_sector','sub_sector')
	search_fields = ('ticker','name','industry','sub_sector','super_sector')


class ArticleAdmin(admin.ModelAdmin):
	list_display = ('date','company','title',)
	list_filter = ('date',)
	search_fields = ('date','company__name','title','url',)

class PriceAdmin(admin.ModelAdmin):
	list_display = ('company', 'date', 'price')
	list_filter = ('date',)
	search_fields = ('company__name','date',)

class ValenceAdmin(admin.ModelAdmin):
	list_display = ('company', 'word', 'valence', 'percent_valence','affected_date',)
	list_filter = ('published_date','affected_date','company__industry','company__super_sector','company__sub_sector',)
	search_fields = ('word','published_date','affected_date','company__name',)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Valence, ValenceAdmin)
		
