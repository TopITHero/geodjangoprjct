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

		