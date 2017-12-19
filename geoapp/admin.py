
from django.contrib import admin 
from .models import Picture,WorldBorder, UserProfile
# Register your models here.
from leaflet.admin import LeafletGeoAdmin

class PictureAdmin(LeafletGeoAdmin):
	
	list_display = ('title','geom')

class WorldBorderAdmin(LeafletGeoAdmin):
	
	pass


admin.site.register(Picture,PictureAdmin)
admin.site.register(WorldBorder,WorldBorderAdmin)
admin.site.register(UserProfile)		 

