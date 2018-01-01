from django.conf.urls import url, include
from django.contrib import admin
from djgeojson.views import GeoJSONLayerView
from django.views.generic import TemplateView
from .models import Picture
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    
    url(r'^$', views.startpage, name = 'start'),
    url(r'^photodata/$', GeoJSONLayerView.as_view(model=Picture), name = 'data'),
    url(r'^worlddata/$',views.country_data,name = 'worlddata'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^userhome/$', views.userhome, name = 'userhome'),
    url(r'^signup/$', views.signup, name = 'signup'),
    url(r'^userhome/edit/$', views.edit_profile, name = 'editprofile'),
    url(r'^wms_server/$', views.wms_server),
    url(r'^wms/', views.wms),
    url(r'^upload/', views.simple_upload),

]
