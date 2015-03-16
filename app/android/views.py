from django.shortcuts import render
from core.forms import UploadApkForm
from core.utils import extract_file
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import Context
from django.contrib.auth.decorators import login_required
from core.models import *
# Create your views here.

def home(request):
    if request.method=="POST":
        form = UploadApkForm(request.POST, request.FILES)
        if form.is_valid():
            new_apk = form.save()
            request.session['apkid'] = new_apk.pk
            print new_apk.apk
            return HttpResponseRedirect('/details/')
        else:
            return render_to_response('home.html', {'form':form}, context_instance=RequestContext(request))
    else:
        form = UploadApkForm()
        return render_to_response('home.html', {'form':form}, context_instance=RequestContext(request))

def details(request):
    if 'apkid' not in request.session:
        return HttpResponseRedirect('/')
    response = extract_file(UploadApk.objects.get(id=request.session['apkid']))
    return render_to_response('details.html', {'response':response}, context_instance=RequestContext(request))
