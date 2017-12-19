from django.contrib.gis.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Picture(models.Model):

	title = models.CharField(max_length = 50)
	description = models.TextField()
	image = models.ImageField()
	geom = models.PointField(srid=4326)
	objects = models.GeoManager()
    
	@property
	def pupupcontent(self):
		return '<p>{}</p>'.format(self.description)




class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name		


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length = 100, default = '')
    city = models.CharField(max_length = 100, default = '')

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwards):
    if kwards['created']:
        user_profile = UserProfile.objects.create(user = kwards['instance'])

post_save.connect(create_profile, sender = User) 


