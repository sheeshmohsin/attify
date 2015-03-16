import os
import urllib

from django.shortcuts import render
from core.forms import UploadApkForm, EditorForm
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
from django.views.decorators.csrf import csrf_exempt
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
    request.session['browse_dir'] = response['output_dir']
    return render_to_response('details.html', {'response':response, 'editor':EditorForm}, context_instance=RequestContext(request))

@csrf_exempt
def dirlist(request):
   r=['<ul class="jqueryFileTree" style="display: none;">']
   try:
       r=['<ul class="jqueryFileTree" style="display: none;">']
       d=urllib.unquote(request.POST.get('dir','c:\\temp'))
       print "browse_dir", d
       for f in os.listdir(d):
           ff=os.path.join(d,f)
           if os.path.isdir(ff):
               r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
           else:
               e=os.path.splitext(f)[1][1:] # get .ext and remove dot
               r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
       r.append('</ul>')
   except Exception,e:
       r.append('Could not load directory: %s' % str(e))
   r.append('</ul>')
   return HttpResponse(''.join(r))

@csrf_exempt
def filecontent(request):
    filepath = request.POST['filepath']
    request.session['current_file'] = filepath
    open_file = open(filepath)
    content = open_file.read()
    print content
    open_file.close()
    return HttpResponse(content)

def setcontent(request):
    if request.method=='POST':
        code = request.POST['code']
        filepath = request.session['current_file']
        open_file = open(filepath, 'w')
        open_file.write(code)
        open_file.close()
        return HttpResponseRedirect('/details/')
    else:
        return HttpResponseRedirect('/details/')
