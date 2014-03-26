from django.db import models

class Company(models.Model):
	"NAME","TICKER","COUNTRY","ICB","INDUS","SUP SEC","SEC","SUB SEC"
	name = models.CharField(max_length=100)
	ticker = models.CharField(max_length=10)
	country = models.CharField(max_length=50)
	icb = models.IntegerField()
	industry = models.CharField(max_length=50)
	super_sector = models.CharField(max_length=50)
	sub_sector = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name;

	class Meta:
		verbose_name_plural = ('Companies')



class Price(models.Model):
    class Meta:
        verbose_name = ('Price')
        verbose_name_plural = ('Prices')

    company = models.ForeignKey(Company)
    price = models.DecimalField(max_digits=10,decimal_places=3)
    date = models.DateField()

    def __unicode__(self):
        return "%s<%s> : %s" % (self.company,self.date,self.price)

class Article(models.Model):
    class Meta:
        verbose_name = ('Article')
        verbose_name_plural = ('Articles')

    def __unicode__(self):
        return "%s :: %s :: %s" % (str(self.date),self.company.name,self.title)
    
    company = models.ForeignKey(Company)
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=500)
    date = models.DateField()

class Valence(models.Model):
    class Meta:
        verbose_name = ('Valence')
        verbose_name_plural = ('Valences')

    def __unicode__(self):
        pass
    
    company = models.ForeignKey(Company)
    article = models.ForeignKey(Article)
    word = models.CharField(max_length=100)
    valence = models.DecimalField(max_digits=10,decimal_places=3)
    percent_valence = models.DecimalField(max_digits=5,decimal_places=2)
    published_date = models.DateField()
    affected_date = models.DateField()