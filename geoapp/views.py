from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required

from .models import Picture,WorldBorder
from .forms import EditUserForm
from math import *

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .EXIF import *

from .shapehandler import *

def startpage(request):

	point = Picture.objects.all()
	return render(request, "home.html",{"point":point})

def country_data(request):
	bourders = serialize('geojson', WorldBorder.objects.all())
	return HttpResponse(bourders,content_type = 'json')	
	
def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],)
			login(request, new_user)
			return redirect('/userhome')
	else:
		form = UserCreationForm()
		args = {'form': form}
		return render(request,'signup.html', args)

def wms_server(query):
	request=query.GET.get('request')
	if request == "GetCapabilities":
		return HttpResponse(open('geoapp/capabilities.xml').read(), content_type='text/xml')
	elif request == "GetLegendGraphic":
		image_data = open("geoapp/legend.png", "rb").read()
		return HttpResponse(image_data, content_type="image/png")
	elif request == "GetFeatureInfo":
		from django.core import serializers
		data = serializers.serialize("xml", Picture.objects.all())
		from django.core.files import File
		f = open('geoapp/pictures.xml', 'w')
		myfile = File(f)
		myfile.write(data)
		myfile.close()
		return HttpResponse(open('geoapp/pictures.xml').read(), content_type='text/xml')
	elif request == 'GetMap':
		bbox =  query.GET.get('bbox')
		z =int(query.GET.get('z'))
		lat=float(query.GET.get('lat'))
		lon=float(query.GET.get('lon'))
		x = (lon+165)*pow(2,z)//360 #135
		y = (105-lat)*pow(2,z)//180 #90+14.4
		image_data = open("mediafiles/QTiles/"+str(z)+"/"+str(int(x))+"/"+str(int(y))+".png", "rb").read()
		return HttpResponse(image_data, content_type="image/png")
def wms(request):
	capabilities_url = "wms_server/?request=GetCapabilities"
	getmap_url = "wms_server/?request=GetMap&z=3&lon=15&lat=20"
	featureinfo_url = "wms_server/?request=GetFeatureInfo"
	legend_url = "wms_server/?request=GetLegendGraphic"
	args = {
		"capabilities_url":capabilities_url, "getmap_url": getmap_url, "featureinfo_url": featureinfo_url, "legend_url": legend_url,
	}
	return render(request, 'wms.html', args)

@login_required
def userhome(request):
	args = {'user': request.user}
	return render(request, 'userhome.html', args)

def edit_profile(request):

	if request.method == "POST":
		form = EditUserForm(request.POST, instance = request.user)

		if form.is_valid():
			form.save()
			return redirect('/userhome')
	else:

		form = EditUserForm(instance = request.user)

		args = {'form':form}

		return render(request,"edit.html", args)		


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        shphand(uploaded_file_url)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')