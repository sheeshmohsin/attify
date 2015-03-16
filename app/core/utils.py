import os
import uuid
from os.path import join
from django import forms
from core.models import *
from django.conf import settings
from bs4 import BeautifulSoup

def get_upload_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('apks/', filename)

def validate_file_extension(value):
    if not value.name.endswith('.apk'):
        raise forms.ValidationError(u'Please upload a .apk extension file')

def extract_file(obj):
	activities = []
	apkdetails = dict()
	filepath = str(obj.apk)
	b = str(filepath).split(".")
	output_dir = 'output/' + str(b[0].lstrip('apks/'))
	android_file = join(settings.MEDIA_ROOT, filepath)
	outputpath = join(settings.MEDIA_ROOT, output_dir)
	command = 'apktool d %s -o %s' % (android_file, outputpath)
	os.system(command)
	manifest_path = join(outputpath, 'AndroidManifest.xml')
	soup = BeautifulSoup(open(manifest_path))
	for activity in soup.find_all('activity'):
		activities.append(activity.get('android:name'))
	apkdetails['activities'] = activities
	apkdetails['output_dir'] = outputpath
	return apkdetails